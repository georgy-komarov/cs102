import requests
from bs4 import BeautifulSoup


def extract_news(parser):
    """ Extract news from a given web page """
    news_list = []

    titles = parser.find_all("tr", {"class": "athing"})
    subtitles = parser.find_all("td", {"class": "subtext"})

    assert len(titles) == len(subtitles)

    for i in range(len(titles)):
        news_item, subtitle_item = titles[i], subtitles[i]

        title = news_item.find("a", {"class": "storylink"}).text

        author_item = subtitle_item.find("a", {"class": "hnuser"})
        author = author_item.text if author_item else ""

        comments_item = subtitle_item.find_all("a")[-1].text.split()
        comments = comments_item[0] if len(comments_item) == 2 else 0

        points_item = subtitle_item.find("span", {"class": "score"})
        points = int(points_item.text.split()[0]) if points_item else 0

        url = news_item.find("a", {"class": "storylink"})["href"]
        if len(url.split(".")) == 1:  # check if relative link
            url = "https://news.ycombinator.com/" + url

        news_list.append(
            {
                "title": title,
                "author": author,
                "comments": comments,
                "points": points,
                "url": url
            }
        )

    return news_list


def extract_next_page(parser):
    """ Extract next page URL """
    return parser.find('a', {"class": "morelink"})["href"]


def get_news(url, n_pages=1):
    """ Collect news from a given web page """
    news = []
    while n_pages:
        print("Collecting data from page: {}".format(url))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        news_list = extract_news(soup)
        next_page = extract_next_page(soup)
        url = "https://news.ycombinator.com/" + next_page
        news.extend(news_list)
        n_pages -= 1
    return news


if __name__ == '__main__':
    news = get_news(url='https://news.ycombinator.com/news', n_pages=20)
