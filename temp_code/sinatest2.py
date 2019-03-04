# !/usr/bin/python
# -*- encoding: utf-8 -*-
"""
    author: conglin du
    license: (C) Copyright 2018-2020, Shanghai hot nest network technology co. LTD.
    contact: gduxiansheng@gmail.com or 2544284522@qq.com
    file: sinatest2.py
    time: 2018-08-03 16:34
"""

import requests
from lxml import etree

headers2 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Host': 'tech.sina.com.cn',
}

headers3 = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    'Host': 'chuangye.sina.com.cn',
}

def get_banner():
    u = 'http://chuangye.sina.com.cn/'
    res = requests.get(url=u, headers=headers3)
    tree = etree.HTML(res.content)

    a = tree.xpath('//div[@class="blk_tw_pic btw01"]/a')
    if a:
        for u in a:
            item = {}
            item['title'] = u.xpath('.//img/@alt')[0]
            item['url'] = u.xpath('./@href')[0]
            item['cover_img'] = u.xpath('.//img/@src')[0]
            item["category"] = None
            res1 = requests.get(url=item['url'], headers=headers2)
            treee = etree.HTML(res1.text)
            author = treee.xpath("//span[@class='source']/a/text()")
            if author:
                item['author'] = author[0]
            ti = treee.xpath("//span[@class='date']/text()")
            if ti:
                ttt1 = str(ti[0].strip() + ':00')
                print ttt1
            for s in item.items():
                print s

if __name__ == '__main__':
    get_banner()
