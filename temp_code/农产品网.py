# -*- coding=utf-8 -*-

import requests, re
from lxml import etree
import pymysql
import time
import redis
from hashlib import md5
import datetime
import jsonpath, json


class SimpleHash(object):
    def __init__(self, cap, seed):
        self.cap = cap
        self.seed = seed

    def hash(self, value):
        ret = 0
        for i in range(len(value)):
            ret += self.seed * ret + ord(value[i])
        return (self.cap - 1) & ret


class NCPSpider():
    def __init__(self, host='127.0.0.1', port=6379, db=0, blockNum=1, key='bloomfilter'):
        self.baseurl = "http://www.zgncpw.com"
        self.headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept - Encoding": "gzip, deflate, sdch",
            "Accept - Language": "zh-CN,zh;q=0.8",
            'Cache-Control': 'max-age=0',
            "Connection": "keep-alive",
            'Host': 'www.zgncpw.com',
            # 'Cookie':'yjs_ab_lid=3786cc63b09423f2eb8fa581ef32a703556f0; yjs_ab_score=300; __cfduid=d24e32664d89c3126c9ce5ae3fd06b4b71540176518; cf_clearance=f16e16f4976568b9ef9f49e1aa21f99cc9b2ad4f-1540176524-31536000-150; yjs_id=128cb64a069bdf0ccb015ba5c1003803; ctrl_time=1; bdshare_firstime=1540176529860; ASP.NET_SessionId=5tmnqwn5rxoctpnabh4zkzhp; Hm_lvt_24b7d5cc1b26f24f256b6869b069278e=1540179041; Hm_lpvt_24b7d5cc1b26f24f256b6869b069278e=1540179249; cf_use_ob=0; __utma=247588352.7612405.1540176530.1540191686.1540195824.4; __utmc=247588352; __utmz=247588352.1540176530.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); Hm_lvt_eda63048a2a5f2f971045c7b18e63a72=1540176529; Hm_lpvt_eda63048a2a5f2f971045c7b18e63a72=1540196779',
            'Referer': 'http://www.zgncpw.com/sell/',
            'Upgrade-Insecure-Requests': '1',
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"}
        self.server = redis.Redis(host=host, port=port, db=db)
        self.bit_size = 1 << 31  # Redis的String类型最大容量为512M，现使用256M
        self.seeds = [5, 7, 11, 13, 31, 37, 61]
        self.key = key
        self.blockNum = blockNum
        self.hashfunc = []
        for seed in self.seeds:
            self.hashfunc.append(SimpleHash(self.bit_size, seed))

    def isContains(self, str_input):
        if not str_input:
            return False
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        ret = True
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            ret = ret & self.server.getbit(name, loc)

        return ret

    def insert(self, str_input):
        m5 = md5()
        m5.update(str_input)
        str_input = m5.hexdigest()
        name = self.key + str(int(str_input[0:2], 16) % self.blockNum)
        for f in self.hashfunc:
            loc = f.hash(str_input)
            self.server.setbit(name, loc, 1)

    def get_url_list(self):

        url_list = []

        # 时政
        for i in range(1, 3496):
            url_temp = "http://www.zgncpw.com/sell/?page={}".format(i)
            url_list.append(url_temp)

        return url_list

    def parse_url(self, url):
        try:
            print('暂停五秒', url)
            time.sleep(5)
            response = requests.get(url=url, headers=self.headers)

            if response.status_code == 200:
                print(response.status_code)
                response.encoding = response.apparent_encoding
                print("ok")
                return response
            else:
                print('请求失败')
                return None
        except requests.exceptions as es:
            print('请求出错', es)

    def getHtml1(self, html):

        if html:
            # try:
            htm = etree.HTML(html)
            print("开始解析中国农产品网")

            li_list = htm.xpath("//ul[@class='li-list-informaition']/li")

            for i in li_list:
                sc = []
                peo = {}
                # 通过列表长度取下标
                #     peo["title"] = i.xpath("//span[@id='layout']/text()")[0]
                #     if i.xpath("./span[@class='k_1']/text()"):
                #         peo["time"] = i.xpath("./span[@class='k_1']/text()")[0]
                #         print(peo["time"])
                #     else:
                #         peo["time"] = "没有时间"
                #     if i.xpath("./span[@class='k_2']//text()"):
                #         peo["variety"] = i.xpath("./span[@class='k_2']//text()")[0]
                #         print(peo["variety"])
                #     else:
                #         peo["variety"] = "没有种类"
                #     peo['place']=i.xpath('./span[3]/a//text()')[0]
                #     peo["variety"] = i.xpath("./a[2]//div[@class='pad-t-d-10 text-align-c clearfix']/h1/text()")[0]

                url = i.xpath("./a[2]/@href")[0]
                # print(url)
                if 'http' not in url:

                    peo["href"] = self.baseurl + url
                else:
                    peo["href"] = url

                print(peo["href"])
                # peo['low_price']=i.xpath('./span[4]/text()')[0]
                # print(peo["low_price"])
                # peo['high_price']=i.xpath('./span[5]/text()')[0]
                # print(peo["high_price"])
                # peo['average_price']=i.xpath('./span[6]/text()')[0]
                # print(peo["average_price"])
                # peo['measure']=i.xpath('./span[7]/text()')[0]
                # print(peo["measure"])
                # href=i.xpath('./span[8]//a/@href')[0]
                # peo['href']=self.baseurl+href
                # print(peo["href"])

                if self.isContains(peo["href"].encode('utf-8')):
                    print('exists!')
                else:
                    print('not exists!')
                    self.insert(peo["href"].encode('utf-8'))
                    time.sleep(5)
                    print("暂缓5秒")
                    # try:
                    if peo['href']:
                        resp = requests.get(url=peo["href"], headers=self.headers)
                        resp.encoding = resp.apparent_encoding
                        resp = resp.text

                        hm = etree.HTML(resp)
                        if hm.xpath("//div[@class='fxr font clearfix']//h1//text()"):
                            detai = hm.xpath("//div[@class='fxr font clearfix']//h1//text()")[0]
                            peo["variety"] = re.sub(
                                r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——?【】？、~@#￥%……&*（）]+|\\n+|\\r+|\\t+|(\\xa0)+|(\\u3000)",
                                "", str(detai))
                        elif hm.xpath("/html/body/div[10]/div[1]/div[1]/div[2]/h1///text()"):
                            detai = hm.xpath("/html/body/div[10]/div[1]/div[1]/div[2]/h1//text()")[0]
                            peo["variety"] = re.sub(
                                r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——?【】？、~@#￥%……&*（）]+|\\n+|\\r+|\\t+|(\\xa0)+|(\\u3000)",
                                "", str(detai))
                        else:
                            detai = hm.xpath("//div[@id='big_div']/..//h1//text()")[0]
                            peo["variety"] = re.sub(
                                r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——?【】？、~@#￥%……&*（）]+|\\n+|\\r+|\\t+|(\\xa0)+|(\\u3000)",
                                "", str(detai))
                        # peo["variety"] = \
                        # hm.xpath("//div[@class='fxr font clearfix']/h1/text()")[0]

                        peo["img"] = hm.xpath("//ul[@class='clearfix']/li[1]/a/img/@src")[0]
                        peo["price"] = hm.xpath("//ul[@class='two l-big line-height-36 clearfix']/li[1]/text()")[0]
                        if hm.xpath("//ul[@class='two l-big line-height-36 clearfix']//li[2]//text()")[0]:
                            peo["qipi"] = hm.xpath("//ul[@class='two l-big line-height-36 clearfix']//li[2]//text()")[0]
                        else:
                            peo["qipi"]='没有相关数据'
                        if hm.xpath("//ul[@class='two l-big line-height-36 clearfix']/li[3]//text()")[0]:
                            peo["total"] = hm.xpath("//ul[@class='two l-big line-height-36 clearfix']//li[3]//text()")[0]
                        else:
                            peo["total"]='没有库存数据'
                        # peo["place"] = hm.xpath("//ul[@class='two l-big line-height-36 clearfix']/li[5]/text()")[0]
                        pla = hm.xpath("//ul[@class='two l-big line-height-36 clearfix']//li[5]//text()")[0]
                        peo["place"] = re.sub(
                            r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——?【】？、~@#￥%……&*（）]+|\\n+|\\r+|\\t+|(\\xa0)+|(\\u3000)",
                            "", str(pla))
                        peo["time"] = hm.xpath("//ul[@class='two l-big line-height-36 clearfix']//li[7]//text()")[0]

                        sc.append([
                            [peo["variety"]], [peo["href"]],
                            [peo["img"]], [peo["price"]], [peo["qipi"]], [peo["total"]], [peo["place"]],
                            [peo["time"]],

                        ])
                        print(sc)
                        conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='box_office',
                                               charset="utf8")

                        cur = conn.cursor()
                        print("插入中")

                        sql = """INSERT INTO zgncp (variety,href,img,price,qipi,total,place,time) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""

                        cur.executemany(sql, sc)
                        conn.commit()

                        cur.close()
                        print("插入成功")
                        conn.close()

                    # except Exception as e:
                    #     print("地址异常",e)
                    #     time.sleep(2)
                    #     continue
        # except Exception as e:
        #     print('解析异常',e)
        #     pass

    def run(self):
        url_list = self.get_url_list()
        print("开始遍历")
        for i in url_list:
            print("第1栏")
            response = self.parse_url(i)
            if response != None:
                text_str = response.text
                r = self.getHtml1(text_str)


if __name__ == '__main__':
    spider = NCPSpider()
    print("开始执行")
    spider.run()
