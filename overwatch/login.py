# coding: utf-8
import requests


class Career(object):
    def __init__(self):
        self.open_url = 'https://www.battlenet.com.cn/login/zh/'
        self.login_url = 'https://www.battlenet.com.cn/login/zh/'
        self.request_url ='https://www.battlenet.com.cn/login/zh/?ref=https://www.battlenet.com.cn/oauth/authorize?client_id%3Dnetease-d3-site%26response_type%3Dcode%26scope%3Did%2Bbattletag%2Blogout%26redirect_uri%3Dhttps%253A%252F%252Faccount.bnet.163.com%252Fbattlenet%252Flogin%253Finner_client_id%253Dow%2526inner_redirect_uri%253Dhttp%25253A%25252F%25252Fow.blizzard.cn%25252Fbattlenet%25252Flogin%25253Fredirect_url%25253Dhttp%2525253A%2525252F%2525252Fow.blizzard.cn%2525252F&app=oauth'
        self.career_url = 'https://www.battlenet.com.cn/account/management/'
        self.headsers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6,zh;q=0.4',
            'Cache-Control': 'no-cache',
            'Connection': 'keep-alive',
            'Content-Length': '792',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cookie': 'JSESSIONID=09c73830-0879-4453-8e4c-8fbf916b1253.blade13_14_login; bnet.extra=AdCfL7grl__OqoQXsnkTvOAWl3SM6UjLuIPIl4ChyT0xfJlqfmZ3iy_dUiMiDi7ceD26ogzDugAxGkPgXhc8zn2ep8deuLapxwkf18itv2fF; web.id=CN-1e5357dc-9ee5-46df-a314-3d8fd3a68b16; eu-cookie-compliance-agreed=1; JSESSIONID=045FEC56CA24BF449D72AC728EDB3770.blade09_02_bnet; xstoken=611c5d4c-034b-4c63-a4bb-b9602cedf43e; __utma=124133273.1188367302.1489716724.1490888418.1490888418.1; __utmc=124133273; __utmz=124133273.1490888418.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); loginChecked=1; _gat_UA-50249600-1=1; _ga=GA1.3.1188367302.1489716724; _gali=submit',
            'Host': 'www.battlenet.com.cn',
            'Pragma': 'no-cache',
            'Referer': 'https://www.battlenet.com.cn/login/zh/?ref=https://www.battlenet.com.cn/oauth/authorize?client_id%3Dnetease-d3-site%26response_type%3Dcode%26scope%3Did%2Bbattletag%2Blogout%26redirect_uri%3Dhttps%253A%252F%252Faccount.bnet.163.com%252Fbattlenet%252Flogin%253Finner_client_id%253Dow%2526inner_redirect_uri%253Dhttp%25253A%25252F%25252Fow.blizzard.cn%25252Fbattlenet%25252Flogin%25253Fredirect_url%25253Dhttp%2525253A%2525252F%2525252Fow.blizzard.cn%2525252F&app=oauth',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36',
            'DNT': '1'
        }
        self.form_data = {
            'accountName': '15113697090@sohu.com',
            'useSrp': 'true',
            'password': '。。。。。。。。。',
            'publicA': '72cb5ee2a01284116214d324463424d28205da458295a7c70108ab4ff9429525939eefe9028a8a6cece4f935b025e00bf2ce98f43b82b5df90444d3ca52d9824a1e0a3d1aeee75274a4a6d321fe00ada6edfefffcb63dc572da9ee03f51fa53b2676f2064e0e96785bc40227c3c5a07e181eee6fcd7954d2e230f8106d619470clientEvidenceM1:efa46bc85654f99a6803cadebde57bcfb1a93db361f80f528fa6449eb6510f7d',
            'clientEvidenceM1': 'e4b6943bec6d62448c2399af69fb89164ad9cb912fc0a6ff9339a7917015296',
            'persistLogin': 'on',
            'sessionTimeout': '1490893172555',
            'csrftoken': 'cce3b8fa-5e55-4c45-b148-47e1b02548cc',
            'fp': '{"0":"DQH+ei","1":"Bv0cj1","2":"CEURno","3":"Bxc2Lc","4":"pmXLX","5":"BEejbW","6":"CXF2Ft","7":"Dvd85Q","10":"DVYZ4X","11":"DXpz63","12":"DbucDB"}',
        }

    def login(self):
        session = requests.session()
        session.headers.update(self.headsers)
        # a = session.post(url=self.request_url, data=self.form_data)
        # print(a.text)
        s = session.get(url='http://ow.blizzard.cn/career/')
        # html = session.get(url=self.career_url)
        print(s.text)
        # print(html.text)
        # html = s.get(url=self.career_url)
        # print(html.text)


instance = Career()
instance.login()
