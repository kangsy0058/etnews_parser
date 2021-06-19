import feedparser
from bs4 import BeautifulSoup
import requests
import threading
import time
import json

def rssparser(url):
    links_authors = list()

    d = feedparser.parse(url)
    for i in d.entries:
        links_authors.append([i['link'], i['author']])


    return links_authors


def contentcrawler(link_author, article_data, error_log_data):
    # parsing data
    soup = BeautifulSoup((requests.get(link_author[0])).text, 'html.parser')
    
    #exception------
    try:

        # header
        header = soup.find_all('header', class_='article_header')
        
        image = soup.find_all('figure', class_='article_image')
        image = image[0].img['src']
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
            "link" : link_author[0]
            })

    else:

        if not content:
            error_log_data['log'].append({
            "title" : title,
            "log" : '--- no content ---',
            "link" : link_author[0]
            })


        else:
            article_data['articles'].append({
            'title' : title,
            'date' : date,
            'author' : link_author[1],
            'image' : image,
            'contents' : content,
            'link' : link_author[0],
            })



if __name__ == '__main__':

    date = time.strftime('%Y-%m-%d', time.localtime(time.time()))


    error_log_data = {'date' : date, "log" : []}
    #---------------- artucle datas -------------
    today_article_data = {'articles':[]}
    today_recommanded_data = {'articles':[]}
    broadcast_article_data = {'articles':[]}
    software_article_data = {'articles':[]}
    matarial_article_data = {'articles':[]}
    electronics_article_data = {'articles':[]}
    economy_jarticle_data = {'articles':[]}
    industry_article_data = {'articles':[]}

    #---------------- json file path ------------
    today_json_file_path = './today_json_data.json'
    today_recommanded_json_file_path = './today_recommanded_json_data.json'
    broadcast_json_file_path = './broadcast_json_data.json'
    software_json_file_path = './software_json_data.json'
    matarial_json_file_path = './matarial_json_data.json'
    electronics_json_file_path = './electronics_json_data.json'
    economy_json_file_path = './economy_json_data.json'
    industry_json_file_path = './industry_json_data.json'

    error_log_file_path = './error_log.txt'

    # ---------------- rss links -----------------
    #오늘의 뉴스
    today_url = 'http://rss.etnews.com/Section901.xml'
    #오늘의 추천기사
    today_recommanded_url = "http://rss.etnews.com/Section904.xml"
    #통신&방송
    broadcast_url = 'http://rss.etnews.com/03.xml'
    #SW&게임&성장기업
    software_url = 'http://rss.etnews.com/04.xml'
    #소재&부품
    matarial_url = 'http://rss.etnews.com/06.xml'
    #전자&자동차&유통
    electronics_url = 'http://rss.etnews.com/60.xml'
    #경제&금융
    economy_url = 'http://rss.etnews.com/02.xml'
    #산업&과학&정책
    industry_url = 'http://rss.etnews.com/20.xml'

    #--------------- setting data ---------------
    urls = [today_url, today_recommanded_url, broadcast_url, software_url, matarial_url, electronics_url, economy_url, industry_url]
    datas = [today_article_data, today_recommanded_data, broadcast_article_data, software_article_data, matarial_article_data, electronics_article_data, economy_jarticle_data, industry_article_data]
    paths = [today_json_file_path, today_recommanded_json_file_path, broadcast_json_file_path, software_json_file_path, matarial_json_file_path, electronics_json_file_path, economy_json_file_path, industry_json_file_path]
    # ------------ data crawling code ------------

    for i in range(8):
        print(f'processing :  {i}')
        links_authors = rssparser(urls[i])
        for link_author in links_authors:
            th = threading.Thread(target=contentcrawler, name=f'{link_author[0]}', args=(link_author, datas[i], error_log_data))
            th.run()

        with open(paths[i], 'w', encoding='utf-8') as json_file:
            json.dump(datas[i], json_file, indent=4, ensure_ascii=False)

    with open(error_log_file_path, 'a', encoding='utf-8') as log_file:
        json.dump(error_log_data, log_file, indent=4, ensure_ascii=False)
        
    print("finish")
