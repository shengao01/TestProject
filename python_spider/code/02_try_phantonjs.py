# coding=utf-8
from selenium import webdriver

driver = webdriver.PhantomJS()

#设置窗口大小
# driver.set_window_size(1920,1080)
#最大化窗口
driver.maximize_window()

driver.get("https://www.v2ex.com/go/python")

#获取页面源码
# print(driver.page_source)
print(driver.get_cookies())
print({i["name"]:i["value"] for i in driver.get_cookies()})
#页面截屏
driver.save_screenshot("./v3.png")
driver.quit()