from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import os
import time
from PIL import Image


class Browser:
    def __init__(self):
        # self.driver = webdriver.Chrome()
        # dcap = dict(DesiredCapabilities.PHANTOMJS)
        # dcap['phantomjs.page.settings.userAgent'] ='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36'
        # self.driver = webdriver.PhantomJS(desired_capabilities=dcap)
        # self.driver = webdriver.PhantomJS()
        self.driver = webdriver.Chrome()
        self.driver.set_window_size(1920, 1080)

    def get_page(self, url):
        self.driver.get(url)

    def get_current_page_shot(self):
        self.driver.save_screenshot('shot.png')
        self.driver.quit()

    def fullapge_shot(self):
        print("Starting chrome full page screenshot workaround ...")

        total_width = self.driver.execute_script("return window.screen.width")
        total_height = self.driver.execute_script("return document.body.parentNode.scrollHeight")
        viewport_width = self.driver.execute_script("return window.screen.width")
        # viewport_width = self.driver.execute_script("return document.body.clientWidth")
        # viewport_height = self.driver.execute_script("return window.innerHeight")
        viewport_height = self.driver.execute_script("return window.screen.availHeight")
        print(
            "Total: ({0}, {1}), Viewport: ({2},{3})".format(total_width, total_height, viewport_width, viewport_height))

        # 得到每个图片的左上角的坐标
        self.driver.save_screenshot('0.png')
        shot = Image.open('0.png')
        width, height = shot.size
        del shot
        heights = []
        y = 0
        while y < total_height:
            heights.append(y)
            y += height
            # 最后一张不完整的图片， 调整坐标
            if y > total_height:
                y = total_height - height

        # 合并图片
        full_image = Image.new('RGB', (width, total_height))
        for h in heights:
            self.driver.execute_script(
                "window.scrollBy({width}, {height})".format(width=0, height=h))
            time.sleep(0.2)
            tmp_img = str(h) + '.png'
            self.driver.get_screenshot_as_file(tmp_img)
            shot = Image.open(tmp_img)
            print(h)

            full_image.paste(shot, (0, h))
            del shot
            os.remove(tmp_img)
        full_image.save('full_shot.png')
        print(self.driver.execute_script("return document.body.parentNode.scrollHeight"))

    def close(self):
        self.driver.quit()


browser = Browser()
# browser.get_page('https://zhuanlan.zhihu.com/p/27914299')
browser.get_page('http://www.bilibili.com/')
browser.fullapge_shot()
browser.close()
