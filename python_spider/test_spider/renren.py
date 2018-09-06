import requests
import re

profile_url = "http://www.renren.com/481421029/profile"
login_url = "http://www.renren.com/PLogin.do"

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
post_data = {"email":"13156505806", "password":"renren2013"}

session = requests.session()
session.post(login_url,headers=headers,data=post_data)

resp = session.get(profile_url,headers=headers)
print(re.findall("张身高",resp.content.decode())) # 查看用户名是否在响应中
