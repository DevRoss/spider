# !/usr/bin/env python
# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
from lxml import html

'''
webdriver登录方式
'''


class BattleNetLogin(object):
    '''登录战网'''

    def __init__(self):
        '''浏览器引擎初始化'''
        self.browser = webdriver.PhantomJS()

    def login(self, url="https://www.battlenet.com.cn/login/zh/"):
        '''登录方法'''
        print("Run..")
        self.browser.get(url)
        form_account = self.browser.find_element_by_id("accountName")
        form_account.send_keys("15113697090@sohu.com")  # 在这儿输入你的用户名
        form_password = self.browser.find_element_by_id("password")
        form_password.send_keys("。。。。。")  # 在这儿输入你的密码
        form_password.send_keys(Keys.RETURN)

        try:
            # 等待新页面生成
            WebDriverWait(self.browser, 5).until(
                expected_conditions.presence_of_element_located((By.ID, "username"))
            )
        except Exception as e:
            # 异常处理，打印错误
            print("Error:".center(60, '='))
            print(e)
            print("=".center(60, "="))
        finally:
            # 登录后页面跳转，获取昵称
            print(self.browser.current_url)  # 打印当前页面的url
            page_dom = html.fromstring(self.browser.page_source)
            nick_name = page_dom.xpath("//div[@id='username']/div[@class='dropdown pull-right']/a/text()")  # 获取昵称
            print(nick_name)

    def __del__(self):
        self.browser.quit()  # 关闭浏览器


if __name__ == '__main__':
    l = BattleNetLogin()
    l.login()
