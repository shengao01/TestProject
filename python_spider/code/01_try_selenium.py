# coding=utf-8
from selenium import webdriver

#实例化driver
driver = webdriver.Chrome()  #mac，linux需要先安装
# webdriver.Chrome(executable_path="chromedriver")  #windows下，传入phantomjs的位置就可以

#请求网址
driver.get("http://www.baidu.com")

#定位元素，输入内容
driver.find_element_by_id("kw").send_keys("传智播客")

#定位元素，点击
driver.find_element_by_id("su").click()

print(driver.current_url)
#退出
driver.quit()