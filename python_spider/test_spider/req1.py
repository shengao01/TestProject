import requests

url = 'http://www.baidu.com/s'
header = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
keywords = input('请输入需要查询的关键字')
params = {'wd':keywords}

response = requests.get(url=url, params=params, headers=header)



# print(response.encoding)
# print('*'*50)
print(response.url)
# print('*'*50)
# print(response.content)
# print('*'*50)

# print(response.text)
# response.data = response.text.encode()

# with open('./cont/111.txt', 'wb') as b:
#     b.write(response.content)
#
# with open('./cont/222.txt', 'wb') as c:
#     c.write(response.data)

print('OK!')