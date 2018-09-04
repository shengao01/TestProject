# coding:utf8
import requests
import re
from bs4 import BeautifulSoup

url = "http://cl.koco.pw/htm_data/7/1712/2866605.html"


class MainSpider():
    def __init__(self):
        self.headers = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    def get_html(self, url):
        # 获取html页面
        resp = requests.get(url, headers=self.headers, timeout=10)
        resp = resp.content.decode()
        return resp

    def re_url(self, html_str):
        # 匹配正则
        # <br><img src='(.*?)'
        # <img src='(.*?)'
        # <input src='(.*?)'
        pattern = re.compile(r"<img src='(.*?)'")
        ret = pattern.findall(html_str)
        print(ret)
        return ret

    def get_girls(self, img_url, file_path):
        img = requests.get(img_url, headers=self.headers, timeout=10)
        img.encoding = 'gbk'
        # soup = BeautifulSoup(res.text, 'html.parser')
        # for images in soup.select('.tpc_content'):
        with open(file_path, 'wb') as code:
            code.write(img.content)
        print('OK!')

    def run(self, url):
        html = self.get_html(url)
        print(html)
        url_list = self.re_url(html)
        for url in url_list:
            name = url[-10:]
            name = "photo/" + name
            self.get_girls(url, name)


if __name__ == '__main__':
    spi = MainSpider()
    spi.run(url)
