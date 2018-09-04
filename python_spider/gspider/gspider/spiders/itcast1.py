# -*- coding: utf-8 -*-
import scrapy
from ..items import GspiderItem


class Itcast1Spider(scrapy.Spider):
    name = 'itcast1'
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):
        li_list = response.xpath("//div[@class='tea_con']//li")
        for li in li_list:
            item = GspiderItem()
            item["name"] = li.xpath(".//h3/text()").extract_first()
            item["title"] = li.xpath(".//h4/text()").extract_first()
            item["profile"] = li.xpath(".//p/text()").extract_first()

            # print(item)
            yield item
