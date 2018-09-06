# coding=utf-8
from selenium import webdriver
driver = webdriver.Chrome()

driver.get("https://www.v2ex.com/go/python")

#find_element 返回一个元素，如果没有，会报错
# t1 = driver.find_element_by_id("TopicsNode")
# print(t1)
# find_elements 返回一个列表，如果没有，返回空列表
# t2 = driver.find_elements_by_id("TopicsNode")
# print(t2)

div_list = driver.find_elements_by_xpath("//div[@id='TopicsNode']/div")
# print(div_list)
# for div in div_list:
#     #获取文本，对元素使用.text获取
#     title = div.find_element_by_xpath(".//span[@class='item_title']/a").text
#     #获取href等属性，对元素使用.get_attrubute("href)
#     href = div.find_element_by_xpath(".//span[@class='item_title']/a").get_attribute("href")
#     print(title,"*"*10,href)

# temp1 = driver.find_element_by_link_text("10")
# print(temp1.get_attribute("href"))
temp2 = driver.find_elements_by_class_name("page_normal")
for a in temp2:
    print(a.get_attribute("href"))
driver.quit()

