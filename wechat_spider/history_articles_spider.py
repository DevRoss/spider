import requests
from bs4 import BeautifulSoup
import re
import json

params = {
    'SCAU': {
        'biz': 'MzIyMjEwMjYxMA',
        'uin': 'MjIxMDM2OTM2MQ%3D%3D',
        'key': 'bfaceaac636432aaf7364292606c0d1679d45c845fee535185129bdd102d4e3fd3888d978c9d1469deab7d1afc7becd835ba69e50551595eefca33ea38e7851c341b3344d6cefbbb523ac3a5feb7f76b',
        'scene': '124&devicetype',
        'pass_ticket': 'HL%2BQHOEcvwQGdCCyp6oFf40BX8gcZdIENpHCDQX1w361iJ%2FBsnIH7meE%2BHiXJ4w7'
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
            self.scene = params[account]['scene']
            self.pass_ticket = params[account]['pass_ticket']

        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'zh-CN,en-US;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'Connection': 'keep-alive',
            'Cookie': 'pgv_pvi=9787430912; pgv_pvid=5941961831; sd_userid=99401491106713589; sd_cookie_crttime=1491106713589; pgv_info=ssid=s4976549360; wap_sid=CNGe/p0IEkB3dERaYm8xZU96MXhxaF9BeTRVb1czZjg5dHdPMUhpWEt2RFpxUWljSjJ2cUxTcHNsay1zeVBYRlk4Xy1ZS3UxGAQg/REo0sS1gAww/bXSxwU=; wap_sid2=CNGe/p0IElxVTVRsQ1RnVXpabjduUjFKdkY0TWUxaHpGNENaMWdYMFBHRmhpZXRyejFpMkhJNERDbGpmZzUwQVNCWVBKaXBjUjNTTjB2UjBTQmh4MnJMRTFudUNTSVFEQUFBfjD9tdLHBQ==',
            'Host': 'mp.weixin.qq.com',
            'X-Requested-With': 'com.tencent.mm',
            'Accept-Encoding': 'gzip, deflate',
            'User-Agent': 'Mozilla/5.0 (Linux; Android 7.1.1; Nexus 5 Build/NOF27B; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 Mobile Safari/537.36 MicroMessenger/6.5.7.1041 NetType/WIFI Language/zh_CN',
            # 'x-wechat-key': '926cd28a4aba000edb9f388d9df05262445a1683abb94e0b9f8589716d739d8ecb2aa758ee89e8268e2583fb6f8ec6e0c56e4620fc0e200adcf07c41e1f1fcfb5354e3b291a55a06cc0b09f4a335fe29',
            # 'x-wechat-uin': 'MjIxMDM2OTM2MQ%3D%3D'
        }
        self.raw_url = 'https://mp.weixin.qq.com/mp/getmasssendmsg?__biz={biz}==&from=1&uin={uin}&key={key}'
        self.raw_history_url = 'https://mp.weixin.qq.com/mp/profile_ext?action=home&__biz={biz}==&scene={scene}=android-25&version=26050741&lang=zh_CN&nettype=WIFI&a8scene=3&pass_ticket={pass_ticket}&wx_header=1'
        self.url = None
        self.session = requests.session()
        self.session.headers.update(self.headers)

    def entrance(self):
        # url合成
        self.url = self.raw_history_url.format(biz=self.biz, uin=self.uin, key=self.key, scene=self.scene,
                                               pass_ticket=self.pass_ticket)
        print(self.url)
        res = self.session.get(url=self.url)
        # res.encoding = 'utf-8'
        error = re.compile('<title>验证</title>')
        print(res.text)
        if re.search(error, res.text) is not None:
            print('url失效')
        msg_list = re.search(r"msgList = '(?P<json>.+)';", res.text)
        print('------------------------------------------------------\n\n\n\n\n')
        print(msg_list.group('json'))
        # article_dict = json.loads(msg_list.group('json'))
        # article_collection = []
        # for article in article_dict['list']:
        #     article_detail = {}
        #     article_detail['content_url'] = article['app_msg_ext_info']['content_url']
        #     article_detail['img'] = article['app_msg_ext_info']['cover']
        #     article_detail['title'] = article['app_msg_ext_info']['title']
        #     for key, value in article_detail.items():
        #         print(key)
        #         print(value)


if __name__ == '__main__':
    starter = Article(account='SCAU')
    starter.entrance()
