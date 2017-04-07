import requests
from bs4 import BeautifulSoup
import re
import json

params = {
    'shiyanlou': {'biz': 'MjM5OTMxMzA4NQ',
                  'uin': 'MjIxMDM2OTM2MQ%3D%3D',
                  'key': 'c634dcb5e6470f9197f6d819adeef44dc7087478f9c4f16e38771fd052d0b0505f91dcb54f0be7addd2118d36bca7fbffa018bf52b203346492905f61770e0faca6cf3cb643b41a27cabc6b80eacc092',

                  }
}

'''
实例化时传入account目标公众号
'''


class Article:
    def __init__(self, account=None):
        self.biz = None
        self.uin = None
        self.key = None
        if account is not None:
            self.biz = params[account]['biz']
            self.uin = params[account]['uin']
            self.key = params[account]['key']

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6,zh;q=0.4',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Cookie': 'wap_sid=CNGe/p0IEkBWUGdsMzdkeU9CV3RoRGlFamJpTDB4UUthLVdSMmM0Qk5hM1JBenFMSEo1aFV5b3A5OXFXU2JJV3drazNTVUlUGAQg/REovbmK+AgwuaKexwU=wap_sid2=CNGe/p0IElwyYkJBMG9mRlZaclhQdkdmSXNybVdnVEhnRUhEQ0toX2lpeDNjY3U0NXZqNjdZd213UWpySVBlTUVNY1g0V01LY1JZTXBPVUpEQklwdUVLa3g3OVBBb01EQUFBfjC5op7HBQ==',
            'DNT': '1',
            'Host': 'mp.weixin.qq.com',
            'Pragma': 'no-cache',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Mobile Safari/537.36',
        }
        self.raw_url = 'http://mp.weixin.qq.com/mp/getmasssendmsg?__biz={biz}==&from=1&uin={uin}&key={key}'
        self.url = None
        self.session = requests.session()
        self.session.headers.update(self.headers)

    def entrance(self):
        # url合成
        self.url = self.raw_url.format(biz=self.biz, uin=self.uin, key=self.key)
        print(self.url)
        res = self.session.get(url=self.url)
        res.encoding = 'utf-8'
        error = re.compile('<title>验证</title>')
        # print(res.text)
        if re.search(error, res.text) is not None:
            print('url失效')
        # history = re.findall('<div class="msg_list js_msg_list">.+', res.text, re.S)
        msg_list = re.search(r'msgList = (?P<json>{(.*?)});', res.text)
        article_dict = json.loads(msg_list.group('json'))
        article_collection = []
        for article in article_dict['list']:
            article_detail = {}
            article_detail['content_url'] = article['app_msg_ext_info']['content_url']
            article_detail['img'] = article['app_msg_ext_info']['cover']
            article_detail['title'] = article['app_msg_ext_info']['title']
            for key, value in article_detail.items():
                print(key)
                print(value)

if __name__ == '__main__':
    starter = Article(account='shiyanlou')
    starter.entrance()
