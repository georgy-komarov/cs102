import os

import bottle
from bottle import route, run, template, redirect, request

from bayes import NaiveBayesClassifier
from db import *
from scraputils import get_news

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


@route('/hello/<name>')
def index(name="Stranger"):
    return template('hello_template', name=name)


@route('/')
@route('/news')
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route('/add_label')
def add_label():
    news_id = request.query['id']
    label = request.query['label']

    s = session()
    new = s.query(News).get(news_id)
    new.label = label
    s.commit()

    redirect('/news')


@route('/update_news/<pages>')
def update_news(pages=1):
    news_list = get_news('https://news.ycombinator.com/newest', n_pages=pages)

    s = session()
    for news_item in news_list:
        news_item_filter = s.query(News).filter(
            News.title == news_item["title"],
            News.author == news_item["author"]).first()

        if news_item_filter is None:
            news = News(title=news_item["title"],
                        author=news_item["author"],
                        url=news_item["url"],
                        comments=news_item["comments"],
                        points=news_item["points"])
            s.add(news)
    s.commit()

    redirect("/news")


@route("/classify")
def classify_news():
    s = session()

    news = s.query(News).filter(News.label != None).all()

    X = []
    y = []

    for element in news:
        X.append(element.title)
        y.append(element.label)

    clf.fit(X, y)

    return redirect('/news')


@route('/recommendations')
def recommendations():
    classified_news = session().query(News).filter(News.label == None).all()

    labels = clf.predict([new.title for new in classified_news])

    for row, label in zip(classified_news, labels):
        row.label = label

    return template('news_recommendations', rows=classified_news)


if __name__ == '__main__':
    bottle.TEMPLATE_PATH.insert(0, os.path.join(PROJECT_DIR, 'templates'))
    clf = NaiveBayesClassifier()
    run(host='localhost', port=8080)
