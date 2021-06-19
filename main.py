import feedparser
from bs4 import BeautifulSoup
import requests
import threading
import time
import json

def rssparser(urls):
    links = list()
    for url in urls:
        d = feedparser.parse(url)
        for i in d.entries:
            links.append(i['link'])

    links = list(set(links))  # 중복제거
    return links


def contentcrawler(link, article_data, error_log_data):
    # parsing data
    soup = BeautifulSoup((requests.get(link)).text, 'html.parser')
    
    #exception------
    try:

        # header
        header = soup.find_all('header', class_='article_header')

        # title
        title = header[0].find_all('h2', class_='article_title')
        title = title[0].get_text()

        # date
        date = header[0].find_all('time', class_='date')
        date = date[0].get_text()
        date = date[6:]

        # content
        cla = soup.find_all('section', class_='article_body')
        cla = (cla[0].find_all('p'))
        content = ''

        for i in cla:
            content += i.get_text(strip=True)

    except IndexError:
        error_log_data['log'].append({
            "log" : 'Index Error',
            "link" : link
            })

    else:

        if not content:
            error_log_data['log'].append({
            "title" : title,
            "log" : '--- no content ---',
            "link" : link
            })


        else:
            article_data['articles'].append({
            'title' : title,
            'date' : date,
            'contents' : content,
            'link' : link
            })



if __name__ == '__main__':

    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))

    json_file_path = f'./json_data/{date}.json'
    error_log_file_path = './error_log.txt'

    article_data = {'articles':[]}
    error_log_data = {'date' : date, "log" : []}


    # ---------------- rss links -----------------
    urls = ('http://rss.etnews.com/Section901.xml',
            'http://rss.etnews.com/Section902.xml',
            'http://rss.etnews.com/Section903.xml',
            'http://rss.etnews.com/Section904.xml',
            'http://rss.etnews.com/03.xml',
            'http://rss.etnews.com/04.xml',
            'http://rss.etnews.com/06.xml',
            'http://rss.etnews.com/60.xml',
            'http://rss.etnews.com/02.xml',
            'http://rss.etnews.com/20.xml',
            'http://rss.etnews.com/25.xml',
            'http://rss.etnews.com/05.xml')

    # ------------ data crawling code ------------

    links = rssparser(urls)
    for link in links:
        th = threading.Thread(target=contentcrawler, name=f'{link}', args=(link, article_data, error_log_data))
        th.run()

    with open(json_file_path, 'w', encoding='utf-8') as json_file:
        json.dump(article_data, json_file, indent=4, ensure_ascii=False)
    with open(error_log_file_path, 'a', encoding='utf-8') as log_file:
        json.dump(error_log_data, log_file, indent=4, ensure_ascii=False)
