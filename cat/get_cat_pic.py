import requests
from bs4 import BeautifulSoup

def get_cat_pic(url):
    session = requests.session()
    session.proxies = {
    'http' : '127.0.0.1:1080',
    'https' : '127.0.0.1:1080'
    }
    rec = session.get(url)
    rec.encoding = 'utf-8'
    soup = BeautifulSoup(rec.content, 'lxml')
    try:
        pic_link = 'https:'+soup.select('.mw-filepage-other-resolutions .mw-thumbnail-link')[-1]['href']
    except IndexError:
        pic_link = 'https:'+soup.select('.fullImageLink a ')[0]['href']
    return pic_link


# url = 'https://zh.wikipedia.org/wiki/File:Ukrainian_Levkoy_cat.jpg'
# print(get_cat_pic(url))