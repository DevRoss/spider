#!/usr/bin/python3
# coding=utf-8
import requests, threading, codecs, time
from lxml import etree
import os

file_path = os.path.dirname(os.path.realpath(__file__))
ip_file_path = os.path.join(file_path, 'ipool.txt')


# 爬取IP
class GetIP(threading.Thread):
    def __init__(self, url, which):
        threading.Thread.__init__(self)
        self.daemon = True
        self.url = url
        self.which = which

    def get_ip(self):
        headers = {'Connection': 'keep-alive',
                   'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'}
        response = requests.get(self.url, headers=headers, timeout=5)
        html = etree.HTML(response.text)
        print('[' + str(response.status_code) + ']' + self.url)
        # 对不同的网址进行爬取
        if self.which is 'xici':
            for tr in html.xpath('//tr[contains(@class, *)]'):
                allIP.append([tr.xpath('./td/text()')[0], tr.xpath('./td/text()')[1]])
        else:
            for tr in html.xpath('//tbody/tr'):
                allIP.append(tr.xpath('./td[contains(@data-title, "IP")]/text()')
                             + tr.xpath('./td[contains(@data-title, "PORT")]/text()'))

    def run(self):
        self.get_ip()


# 验证IP可用性
class CheackIp(threading.Thread):
    def __init__(self, ipList):
        threading.Thread.__init__(self)
        self.daemon = True
        self.ipList = ipList

    def check_ip(self):
        for ip in self.ipList:
            proxy = {'http': ip[0] + ':' + ip[1], 'https': ip[0] + ':' + ip[1]}
            try:
                response = requests.get('http://ip.chinaz.com/getip.aspx', proxies=proxy, timeout=5)
                if response.status_code is 200:
                    print(ip[0] + ':' + ip[1])
                    usefulIP.append(ip[0] + ':' + ip[1])
            except Exception as e:
                pass

    def run(self):
        self.check_ip()


def run_spider_threads():
    for i in range(1, 5):
        xici.append('http://www.xicidaili.com/nn/%d' % i)
        kuai.append('http://www.kuaidaili.com/free/inha/%d/' % i)
    for i in range(len(kuai)):
        threads.append(GetIP(xici[i], 'xici'))
        threads.append(GetIP(kuai[i], 'kuai'))
    for thread in threads:
        thread.start()
        # 快代理会ban访问太快的，只好等待1.5秒
        # 西刺会禁止同IP的多次爬取，所以一天不要爬太多次
        time.sleep(1.5)
    for thread in threads:
        thread.join()


def run_check_threads():
    print('[!]Total crawling %d ip' % len(allIP))
    x = int(len(allIP) / 25)
    for i in range(25):
        # 对IP切片
        threads.append(CheackIp(allIP[x * i:x * (i + 1)]))
    for thread in threads:
        thread.start()
    print('[*]Start threads: %s' % threading.activeCount())
    for thread in threads:
        thread.join()
    print('[*]End threads: %s\n' % threading.activeCount())


def write():
    file = codecs.open(ip_file_path, 'wb', encoding='utf-8')
    for i in usefulIP:
        file.write(i)
        file.write('\n')
    file.close()
    print('[!]These ip had already stored in ipool.txt')


def run_get_proxy():
    global xici
    global kuai
    global allIP
    global usefulIP
    global threads
    xici = []
    kuai = []
    allIP = []
    usefulIP = []
    threads = []
    run_spider_threads()
    threads = []
    run_check_threads()
    write()

# if __name__ == '__main__':
#     xici = []
#     kuai = []
#     allIP = []
#     usefulIP = []
#     threads = []
#     run_spider_threads()
#     threads = []
#     run_check_threads()
#     write()
