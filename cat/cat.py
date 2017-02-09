# coding:utf-8

import requests
from bs4 import BeautifulSoup

cat_wiki = 'https://zh.wikipedia.org/wiki/%E5%AE%B6%E8%B2%93%E5%93%81%E7%A8%AE%E5%88%97%E8%A1%A8'
session = requests.session()
session.proxies = {
    'http' : '127.0.0.1:1080',
    'https' : '127.0.0.1:1080'
}
rec = session.get(cat_wiki)
rec.encoding = 'utf-8'
soup = BeautifulSoup(rec.text, 'html.parser')
# print(soup)
cat_list_raw = soup.select('.mediawiki ltr sitedir-ltr mw-hide-empty-elt ns-0 ns-subject page-家貓品種列表 rootpage-家貓品種列表 skin-vector action-view'.replace(' ','.'))[0].select('#content #bodyContent #mw-content-text')[0]
cat_list = cat_list_raw.select('table')[1].select('tr')[1:]

cat_collection = []
for cat in cat_list:
    cat_detail = {}
    cat_detail['name'] = cat.select('a')[0].text
    cat_detail['country'] = cat.select('td')[1].text
    cat_detail['origin'] = cat.select('td')[2].text.replace('\n',' ')
    cat_detail['body_type'] = cat.select('td')[3].text
    cat_detail['hair'] = cat.select('td')[4].text
    cat_detail['color'] = cat.select('td')[5].text
    cat_collection.append(cat_detail)

    # print(cat_detail['name'],
    #       cat_detail['country'],
    #       cat_detail['origin'],
    #       cat_detail['body_type'],
    #       cat_detail['hair'],
    #       cat_detail['color']
    #       )
# print(cat_collection)
import pandas
df = pandas.DataFrame(cat_collection,
                      columns=['name', 'country', 'origin', 'body_type', 'hair', 'color'])
df.to_excel('cat.xlsx')
