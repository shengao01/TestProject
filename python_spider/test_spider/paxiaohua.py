# coding:utf-8
import requests
from bs4 import BeautifulSoup
import gevent
from gevent import monkey

monkey.patch_all()


def get_girls(girl_url):
    main_url = 'http://www.xiaohuar.com'
    header = {"User-Agent": "Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Trident/5.0;"}
    res = requests.get(girl_url, headers=header, timeout=10)
    res.encoding = 'gb2312'
    soup = BeautifulSoup(res.text, 'html.parser')
    print(res)
    for images in soup.select('.item'):
        image_url = main_url + images.select('.item_t .img a img')[0]['src']
        # print(image_url)
        houzui = image_url[-4:]
        img_alt = images.select('.item_t .img a img')[0]['alt'] + houzui
        print(img_alt)
        print(image_url)
        img = requests.get(image_url)
        with open('./xiaohua/' + img_alt, 'wb') as code:
            code.write(img.content)
    print('OK!')


def url_change():
    for i in range(1, 20):
        url = 'http://www.xiaohuar.com/list-1-' + str(i) + '.html'
        gevent.spawn(get_girls, url).join()


url_change()
