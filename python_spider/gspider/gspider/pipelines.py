# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

logger = logging.getLogger(__name__)


class GspiderPipeline0(object):
    def process_item(self, item, spider):
        # print(spider.name)
        item["s_name"] = spider.name
        # print("this is item", item)
        # print(item)
        # item接受的是爬虫传过来的数据
        # spider是当前启动的爬虫
        return item

class GspiderPipeline1(object):
    def process_item(self, item, spider):
        # print(spider.name)
        # if spider.name == "itcast1":
        #     print("this is item", item)
        # # print(item)
        logger.warning(item)
        # item接受的是爬虫传过来的数据
        # spider是当前启动的爬虫
        return item
