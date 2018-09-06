import requests
import re
from bs4 import BeautifulSoup
import gevent
from gevent import monkey


monkey.patch_all()
main_url = 'http://www.xiaohuar.com'
header = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}


class XiaohuaSpider():
    def get_Girls(self, girl_url):
        res = requests.get(girl_url, headers=header, timeout=10)
        res.encoding = 'gb2312'
        soup = BeautifulSoup(res.text, 'html.parser')
        print(soup)
        for images in soup.select('.item'):
            image_url = main_url + images.select('.item_t .img a img')[0]['src']
            houzui = image_url[-4:]
            img_alt = images.select('.item_t .img a img')[0]['alt'] + houzui
            print(img_alt)
            img = requests.get(image_url)
            with open('./xiaohua1/' + img_alt, 'wb') as code:
                code.write(img.content)
        print('OK!')

    def url_change(self):
        for i in range(22, 23):
            url = 'http://www.xiaohuar.com/list-1-' + str(i) + '.html'
            gevent.spawn(self.get_Girls, url).join()

if __name__ == '__main__':
    spi = XiaohuaSpider()
    spi.url_change()
