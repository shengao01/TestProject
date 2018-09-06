import requests
import re


class DuanziSpider():
    def __init__(self):
        self.header = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}

    # 发送请求获取数据
    def parse_url(self, url):
        resp = requests.get(url, headers=self.header)
        return resp.content.decode()

    # 获取请求的数据,并进行中正则匹配
    def handle_content(self, html_str):
        # pattern = re.compile(r'<a\shref="/article/\d+.html"\sclass="title"\stitle=(.*?)</a></h3>.*?<div\sclass="desc">(.*?)</div>')
        pattern = re.compile(r'<div\sclass="desc">(.*?)</div>')
        t = pattern.findall(html_str)
        dlist = []
        for d in t:
            print(d)
            dlist.append(d)

        return dlist

    def run(self):
        url = "http://www.neihan8.com/wenzi/"
        html_str = self.parse_url(url)
        print(html_str)
        res = self.handle_content(html_str)

        myFile = open('duanzi.txt', 'wb')
        for duanzi in res:
            dz = duanzi.encode()
            myFile.write(dz)
            myFile.write(b'---------------------------------------------')
        myFile.close()
        print('OK!')


if __name__ == '__main__':
    duanzi = DuanziSpider()
    duanzi.run()
