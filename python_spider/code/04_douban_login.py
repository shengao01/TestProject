# coding=utf-8
from selenium import webdriver
import time
import requests
from yundama.dama import  indetify

driver = webdriver.Chrome()
driver.get("https://www.douban.com/")

driver.find_element_by_id("form_email").send_keys("784542623@qq.com")
driver.find_element_by_id("form_password").send_keys("zhoudawei123")

# driver.find_element_by_class_name("bn-submit").click()
#
# time.sleep(3)
# driver.find_element_by_id("password").send_keys("zhoudawei123")

#获取验证码的地址
captcha_url = driver.find_element_by_id("captcha_image").get_attribute("src")
resposne = requests.get(captcha_url)  #图片的bytes字节数
ret = indetify(resposne.content)
print("验证码的识别结果是:",ret)

#驶入验证码
driver.find_element_by_id("captcha_field").send_keys(ret)

#点击登录
driver.find_element_by_class_name("bn-submit").click()

time.sleep(3)
cookies_list = driver.get_cookies()
cookie_dict = {i["name"]:i["value"] for i in cookies_list}
print(cookie_dict)
driver.quit()
