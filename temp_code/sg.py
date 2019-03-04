# -*- coding: utf-8 -*-
import scrapy
from pymongo import MongoClient
import requests
import json
from urllib.parse import quote
from bson import ObjectId


class SgSpider(scrapy.Spider):
    name = 'sg'
    allowed_domains = []
    start_urls = []

    def start_requests(self):
        '''
        # path = os.path.dirname(os.path.realpath(__file__))  # 获取当前路径
        # file_path = os.path.join(path)
        '''
        mon = MongoClient(host='192.168.168.234', port=27017)
        db = mon.probe  # 库
        coll = db.probe_record  # 表
        req = coll.find()  # 读取所有的数据
        for i in req:
            db_one = {
                '_id': ObjectId(i['_id']),
                'probeImgUrl': i['probeImgUrl'],
                'probeStatus': i['probeStatus'],
            }
            url = db_one['probeImgUrl']  # 拿出图片url
            id = db_one["_id"]
            probeStatus = db_one["probeStatus"]
            status = requests.get(url).status_code  # 获取图片地址的请求状态吗
            print(status)
            if status == 200:
                # if probeStatus == 0:
                yield scrapy.Request(
                    url,
                    callback=self.parse,
                    meta={"id": id}
                )

    def parse(self, response):
        item = {}
        item['id'] = response.meta["id"]
        # url   https://ss2.bdstatic.com/70cFvnSh_Q1YnxGkpoWK1HF6hhy/it/u=3811177021,804888149&fm=26&gp=0.jpg
        #       https://ss1.bdstatic.com/70cFuXSh_Q1YnxGkpoWK1HF6hhy/it/u=4063479054,2180565519&fm=26&gp=0.jpg
        src = response.url
        url = quote(src)
        print(url, "=====url")
        # try:
        href = 'http://pic.sogou.com/ris?query={}&dm=0&reqType=ajax&tn=0&reqFrom=result'.format(url)
        # print(href, "=============href")
        result = requests.get(href).content;
        print(result)
        html = result.decode('gbk')  # .replace("0xb5", "").replace("0xb4", "")  # .replace("0xfd", "")
        # print(html,"----------html")
        dicts = json.loads(html)
        lists = dicts["items"]
        all_item = []
        for li in lists:
            item["title"] = li["title"]
            item["tortImgUrl"] = li["page_url"]  # 商品地址
            item["tortImghumbStore"] = li["pic_url"]  # 图片地址
            all_item.append(item)
        items = {"sougou": all_item}
        print(items)
        # yield items
        # except:
        #     print("当前url有问题", href)
