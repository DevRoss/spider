from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time

'''
对某些网页加载有问题
如demo
'''


class Browser:
    def __init__(self):
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap['phantomjs.page.settings.userAgent'] ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        # self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        self.driver = webdriver.PhantomJS()

    def get_page(self, url):
        self.driver.get(url)

    def get_full_page_shot(self):
        total_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        size = self.driver.get_window_size()
        print(size['width'], size['height'])
        y = 0
        # 滚动到最后
        while y < total_height:
            self.driver.execute_script("window.scrollBy({width}, {height})".format(width=0, height=size['height']))
            time.sleep(0.5)
            y += size['height']
            print(y)
            total_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        # time.sleep(0.5)
        self.driver.save_screenshot('full_page.png')

    def close(self):
        self.driver.quit()


browser = Browser()
url = 'http://www.bilibili.com/'
browser.get_page(url)
browser.get_full_page_shot()
browser.close()
