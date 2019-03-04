# -*- coding:utf-8 -*-
import requests
from lxml import html
import re
import woff2otf
from fontTools.ttLib import TTFont

#抓取maoyan票房
class MaoyanSpider:
    #页面初始化
    def __init__(self):
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.8",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1",
            "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36"
        }
    # 获取票房
    def getNote(self):
        url = "http://maoyan.com"
        host = {'host':'maoyan.com',
                'refer':'http://maoyan.com/news',}
        headers = dict(self.headers.items() + host.items())
        # 获取页面内容
        r = requests.get(url, headers=headers)
        # print r
        # print r.text
        response = html.fromstring(r.text)
        # print response
        # 匹配ttf font
        cmp = re.compile(",\n           url\('(//.*.woff)'\) format\('woff'\)")
        print cmp
        rst = cmp.findall(r.text)
        print rst[0]
        ttf = requests.get("http:" + rst[0], stream=True)
        print ttf
        with open("maoyan.woff", "wb") as pdf:
            for chunk in ttf.iter_content(chunk_size=1024):
                if chunk:
                    pdf.write(chunk)
        # 转换woff字体为otf字体
        woff2otf.convert('maoyan.woff', 'maoyan.otf')
        # 解析字体库font文件
        baseFont = TTFont('base.otf')
        maoyanFont = TTFont('maoyan.otf')
        uniList = maoyanFont['cmap'].tables[0].ttFont.getGlyphOrder()
        numList = []
        baseNumList = ['.', '3', '5', '1', '2', '7', '0', '6', '9', '8', '4']
        baseUniCode = ['x', 'uniE64B', 'uniE183', 'uniED06', 'uniE1AC', 'uniEA2D', 'uniEBF8',
        'uniE831', 'uniF654', 'uniF25B', 'uniE3EB']
        for i in range(1, 12):
            maoyanGlyph = maoyanFont['glyf'][uniList[i]]
            for j in range(11):
                baseGlyph = baseFont['glyf'][baseUniCode[j]]
                if maoyanGlyph == baseGlyph:
                    numList.append(baseNumList[j])
                    break
        uniList[1] = 'uni0078'
        utf8List = [eval("u'\u" + uni[3:] + "'").encode("utf-8") for uni in uniList[1:]]
        # 获取发帖内容
        movie_name = response.cssselect(".ranking-box-wrapper li .ranking-top-moive-name")[0].text_content().replace(' ', '').replace('\n', '').encode('utf-8')
        movie_wish = response.cssselect(".ranking-box-wrapper li .ranking-top-wish")[0].text_content().replace(' ', '').replace('\n', '').encode('utf-8')

        print movie_name, movie_wish

        print '---------------after-----------------'
        for i in range(len(utf8List)):
            movie_wish = movie_wish.replace(utf8List[i], numList[i])
        print movie_name, movie_wish


spider = MaoyanSpider()
spider.getNote()
