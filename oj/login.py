# coding: utf-8
import requests
from bs4 import BeautifulSoup


def login():
    login_url = 'http://172.26.14.60:8000/uoj/j_security_check'
    main_page = 'http://172.26.14.60:8000/uoj/mainMenu.html?host='
    rank_url = 'http://172.26.14.60:8000/uoj/user_user_listBySearchUsername_PUBLIC.html?searchKey=username&searchValue=2016%25'
    form_data = {
        'j_username': '。。。。',
        'j_password': '。。。。',
    }
    session = requests.session()

    session.headers = {
        'Host': '172.26.14.60:8000',
        'Connection': 'keep-alive',
        'Content-Length': '69',
        'Cache-Control': 'max-age=0',
        'Origin': 'http://172.26.14.60:8000',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'DNT': '1',
        'Referer': 'http://172.26.14.60:8000/uoj/login.jsp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,en-US;q=0.8,en;q=0.6,zh;q=0.4'
    }

    session.post(url=login_url, data=form_data)
    rank = session.get(url=rank_url)
    soup = BeautifulSoup(rank.text, 'lxml')
    table = soup.select('.table tbody td')
    user_deail = {}
    for user in table:
        user_id = user.select('a')
        if user_id:
            user_deail['userid'] = user_id[0].text
            print(user_deail['userid'])
            # print(user)


if __name__ == '__main__':
    login()
