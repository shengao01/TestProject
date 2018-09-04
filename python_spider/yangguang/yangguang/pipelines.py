# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re
# from pymongo import MongoClient

# client = MongoClient(host='127.0.0.1',port=27017)
# collection = client["spider"]["yangguang"]


class YangguangPipeline(object):
    def process_item(self, item, spider):
        item["content"] = self.process_item_content(item["content"])[0]
        print(item)
        # collection.insert_one(dict(item))
        return item

    def process_item_content(self,content_list):
        content_list = [re.sub(r"\xa0|\s+","",i) for i in content_list]
        content_list = [i for i in content_list if len(i) > 0]

        return content_list