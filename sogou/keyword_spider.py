# coding:utf-8
from bs4 import BeautifulSoup
import requests
import time
import json
import pandas
from urllib.parse import quote
import re
import sys

website_dict = {
    'sogou': 'http://weixin.sogou.com/',

}
# post_url = 'http://119.29.28.134:8000/itemStore/'
# destroy_url = 'http://119.29.28.134:8000/destroy-item/'
post_url = 'http://sfgx.fashcollege.com/itemStore/'
destroy_url = 'http://sfgx.fashcollege.com/destroy-item/'


class SogouSpider(object):
    def __init__(self, website, debug=False, do_post=False, use_proxy=False):
        self.debug = debug
        self.do_post = do_post
        self.website = website
        self.use_proxy = use_proxy
        self.proxies = {
            'http': '127.0.0.1:1080',
            'https': '127.0.0.1:1080',
        }
        self.index_url = website_dict[website]
        self.search_url = 'http://weixin.sogou.com/weixinwap?query={keyword}&type=2'
        self.next_page_url = 'http://weixin.sogou.com/weixinwap?page={page_num}&_rtype=json&query={keyword}&type=2'
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6,zh;q=0.4',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            'DNT': '1',
            'Host': 'weixin.sogou.com',
            'Referer': 'http//weixin.sogou.com/',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 5.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Mobile Safari/537.36',

        }
        self.session = requests.session()
        self.post_headers = {
            'Connection': 'close',
            'Content-Type': 'text/html; charset=UTF-8',
            'X-Powered-By': 'PHP/7.0.11',
            # 'Host': '119.29.28.134:8000',
        }
        self.session.headers.update(self.headers)
        if self.use_proxy:
            self.session.proxies = self.proxies
        if self.debug:
            self.data_frame = pandas.DataFrame([], columns=['title', 'publish_time', 'url', 'from', 'img'])

    def lets_post(self, post_url, data_to_post):
        # 最多重试3次
        for i in range(3):
            try:
                p = requests.post(url=post_url, data=data_to_post, timeout=10)
                print(p.text)
                if p.status_code == 200:
                    break
            except requests.HTTPError or requests.Timeout:
                pass

    def first_page(self, keyword):
        session = self.session
        for i in range(3):
            try:
                rec = session.get(url=self.search_url.format(keyword=keyword), timeout=10)
                rec.encoding = 'utf-8'
                break
            except requests.Timeout:
                pass
        soup = BeautifulSoup(rec.text, 'lxml')
        news_set = soup.select('.pic-list ul li')  # 搜索列表
        news_collection = []
        for news in news_set:
            news_detail = {}
            try:
                news_detail['title'] = news.select('.list-txt h4 a div')[0].text
            except AttributeError:
                break
            news_detail['url'] = news.select('div > h4 > a')[0]['href']
            news_detail['from'] = news.select('.s2')[0]['data-sourcename']
            # 时间取消
            # news_detail['publish_time'] = time.strftime('%Y-%m-%d', time.localtime(
            #     int(news.select('.time .s3')[0]['data-lastmodified'])))
            img_selector = ['.pic > a > img', 'div > div > a > img', 'div div a span div img']
            for selector in img_selector:
                news_img = news.select(selector)
                if len(news_img) != 0:
                    break
            try:
                img_raw = news_img[0]['src']
                img = re.search('&url=(.+)', img_raw)
                news_detail['img'] = img.group(1)
            except IndexError:
                news_detail['img'] = None

            '''
            发送数据
            '''
            if self.do_post:
                self.lets_post(post_url=post_url, data_to_post=news_detail)
            if self.debug:
                news_collection.append(news_detail)
        '''
        将数据放进excel
        '''
        if self.debug:
            df = pandas.DataFrame(news_collection)
            self.data_frame = pandas.concat([self.data_frame, df], ignore_index=True)
            print(self.data_frame)

    def get_more(self, keyword):
        session = self.session
        for page in range(2, 11):
            time.sleep(1)
            next_page_url = self.next_page_url.format(page_num=page, keyword=quote(keyword))
            for i in range(3):
                try:
                    res = session.get(url=next_page_url, timeout=1)
                    res.encoding = 'utf-8'
                    break
                except requests.Timeout:
                    pass
            # 将res.text转化为json
            news_set_as_json = json.loads(res.text)['items']
            news_collection = []
            for news in news_set_as_json:
                news_detail = {}
                soup = BeautifulSoup(news, 'xml')
                news_detail['title'] = re.sub(pattern='大学生', repl='大学生', string=soup.select('title')[0].text)
                news_detail['url'] = soup.select('url')[0].text
                news_detail['from'] = soup.select('sourcename')[0].text
                # 取消时间
                # news_detail['publish_time'] = time.strftime('%Y-%m-%d', time.localtime(
                #     int(re.search('timestamp=(\d{10})&', soup.select('encQrcodeUrl')[0].text).group(1))))
                try:
                    news_detail['img'] = soup.select('imglink')[0].text
                except IndexError:
                    news_detail['img'] = None
                if self.do_post:
                    self.lets_post(post_url=post_url, data_to_post=news_detail)
                if self.debug:
                    news_collection.append(news_detail)

                '''debug 模式'''
            if self.debug:
                df = pandas.DataFrame(news_collection)
                self.data_frame = pandas.concat([self.data_frame, df], ignore_index=True)
                # print(self.data_frame)
                self.save_to_excel()

    def save_to_excel(self):
        self.data_frame.to_excel('ok.xlsx')


if __name__ == '__main__':
    requests.get(url=destroy_url)
    # search = SogouSpider(website='sogou', debug=False, do_post=True)
    # search = SogouSpider(website='sogou', debug=True,do_post=False)
    # search.first_page(keyword='大学生')
    # search.get_more(keyword='大学生')

    search = SogouSpider(website='sogou', debug=False, do_post=True)
    for key_word in sys.argv[1:]:
        print(key_word)
        search.first_page(keyword=key_word)
        # search.get_more(keyword=key_word)
        time.sleep(3)
