import requests
from bs4 import BeautifulSoup


'''
用来获取form中的hidden
'''

def parse_form(url):
    doc = requests.get(url=url)
    doc.encoding = 'utf-8'
    soup = BeautifulSoup(doc.text, 'lxml')
    form_table = soup.select('#password-form input')[2:]
    data = {}
    for e in form_table:
        try:
            data[e['name']] = e['value']
            if len(e['value']) ==0:
                data[e['name']] = '1111111'
        except KeyError:
            data[e['name']] = '23333333'
    for k,v in data.items():
        print(k, v)
    # print(len(form_table))
    # print(form_table)


url = 'https://www.battlenet.com.cn/login/zh/'
parse_form(url)
