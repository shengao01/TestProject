import requests
from lxml import etree

html = etree.parse('hello.html')
print(type(html))

result = html.xpath('//li')
print(result)
print(len(result))
print(type(result))
print(type(result[0]))

result1 = html.xpath('//li/@class')
print(result1)

# res = etree.tostring(html)
# print(res)