# -*- coding: UTF-8 -*-
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.events import EventFiringWebDriver
from selenium.common.exceptions import TimeoutException, WebDriverException
import time


class Weixin(object):
    def __init__(self):
        super(Weixin, self).__init__()
        self.driver = None
        self.url = r'http://huodong.kongzhi.net/2018caiac/tp-page.php?type=solution'
        self.xpath = {
            u'天地和兴': "//div[text()='北京天地和兴科技有限公司']/following-sibling::div//a",
        }

    def toupiao(self):
        self.driver = webdriver.Chrome("chromedriver.exe")
        self.driver.maximize_window()
        self.driver.get(self.url)
        element = self.driver.find_element_by_xpath(self.xpath[u'天地和兴'])
        if element:
            element.click()
            print('点击投票成功')
            time.sleep(2)
            alert = self.driver.switch_to_alert()
            if alert:
                time.sleep(2)
                print (alert.text)  
                alert.accept()   
                time.sleep(2)
        else:
            print('未能找到投票按钮')

if __name__ == '__main__':
    Weixin().toupiao()