import os

import bottle
from bottle import route, run, template, redirect

from db import *

PROJECT_DIR = os.path.dirname(os.path.abspath(__file__))


@route('/')
@route('/hello/<name>')
def index(name="Stranger"):
    return template('hello_template', name=name)


@route('/news')
def news_list():
    s = session()
    rows = s.query(News).filter(News.label == None).all()
    return template('news_template', rows=rows)


@route('/add_label')
def add_label():
    # 1. Получить значения параметров label и id из GET-запроса
    # 2. Получить запись из БД с соответствующим id (такая запись только одна!)
    # 3. Изменить значение метки записи на значение label
    # 4. Сохранить результат в БД
    redirect('/news')


@route('/update_news')
def update_news():
    # 1. Получить данные с новостного сайта
    # 2. Проверить, каких новостей еще нет в БД. Будем считать,
    #    что каждая новость может быть уникально идентифицирована
    #    по совокупности двух значений: заголовка и автора
    # 3. Сохранить в БД те новости, которых там нет
    redirect('/news')


@route("/classify")
def classify_news():
    # PUT YOUR CODE HERE
    redirect("/news")


if __name__ == '__main__':
    bottle.TEMPLATE_PATH.insert(0, os.path.join(PROJECT_DIR, 'templates'))
    run(host='localhost', port=8080)
