# coding:utf-8
import urllib
import urllib2
import cookielib
import getpass
import sys
import chardet
'''
普通request登录
'''

class ow_login():
    def __init__(self):
        self.login_url = "战网通行证登录"
        self.header = {
            'Host': 'www.battlenet.com.cn',
            # 'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393',
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:50.0) Gecko/20100101 Firefox/50.0',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
            'Accept-Encoding': 'gzip, deflate, br',
            'Referer': 'https://www.battlenet.com.cn/login/zh/?ref=https://www.battlenet.com.cn/oauth/authorize?client_id%3Dnetease-sc2-esports%26response_type%3Dcode%26scope%3Did%2Bbattletag%2Blogout%2Bprofile%2Bprivate_games%26redirect_uri%3Dhttps%253A%252F%252Faccount.bnet.163.com%252Fbattlenet%252Flogin%253Finner_client_id%253Dow%2526inner_redirect_uri%253Dhttp%25253A%25252F%25252Fow.blizzard.cn%25252Fbattlenet%25252Flogin%25253Fredirect_url%25253Dhttp%2525253A%2525252F%2525252Fow.blizzard.cn%2525252Fhome%2525252F&app=oauth',
            'Cookie': 'JSESSIONID=842bd059-8eca-4a1f-b690-3e4001c3ff21.blade13_14_login; bnet.extra=AYcmTLNH86xpKRpIg5baUpqFT5W7v6RhLj5oijUlyLp_XvAryg14h4b44R9SWJT2WZMgFbcxAs9asIlxg-vX0gdSlAa6szd5YRJK6vNd670d; web.id=CN-2845ba0a-7216-428d-ad0d-7a345cf27955; _ga=GA1.3.1495478695.1484103423; _gat_bnetgtm=1; _gali=submit; _gat_UA-50249600-1=1',
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1'
        }
        self.post_data = {
            'accountName': '068089dy%40gmail.com',
            'password': '..........',
            'useSrp': 'true',
            'publicA': '570911638ad35aa34f6419543ab4e28b38f286dfa51ec4c5d719becac317368c49727967de5aa0cf038637f8955bfd91ec9c8a65589c2f7288f627db36dd7663b56ddd23b2eabb66c8c49ba59d95955f55054e3e18a0d5bd51e5da528f6a1e5fb19accba935b03817b8d7369c29de0513f5c234359c8ca56aab251417311d8e9',
            'clientEvidenceM1': 'c37c0d4ce7be51a634a7f2f19fedd0fd7679591a49e06f004a88347ef7db86d1',
            'persistLogin': 'on',
            'csrftoken': 'dbbdfcd6-80ad-4d84-afff-f0182fa7f65c',
            'sessionTimeout': '1484131141700',
            'fp': '%7B%220%22%3A%22THBgy%22%2C%221%22%3A%22Bv0cj1%22%2C%222%22%3A%22CEURno%22%2C%223%22%3A%22CgcxR%22%2C%224%22%3A%22pmXLX%22%2C%225%22%3A%22BEejbW%22%2C%226%22%3A%22b%2BbVB%22%2C%227%22%3A%22C0kg%2BZ%22%2C%2210%22%3A%22DVYZ4X%22%2C%2211%22%3A%22DXpz63%22%2C%2212%22%3A%22BtBxZq%22%7D'
        }
        cj = cookielib.CookieJar()
        self.opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))

    def login(self):
        post_data = urllib.urlencode(self.post_data)
        request = urllib2.Request(self.login_url, post_data, self.header)
        resp = self.opener.open(request)
        # resp = self.opener.open(self.login_url,post_data)
        status = resp.getcode()
        if status == 200:
            print("login sussecs!")
            html = resp.read()
            typeEncode = sys.getfilesystemencoding()  ##系统默认编码
            infoencode = chardet.detect(html).get('encoding', 'utf-8')  ##通过第3方模块来自动提取网页的编码
            # html = html.decode(infoencode,'ignore').encode(typeEncode)##先转换成unicode编码，然后转换系统编码输出
            # html = unicode(html,'UTF-8').encode('UTF-8')
            print(html)
            print(infoencode)


ow_login().login()
