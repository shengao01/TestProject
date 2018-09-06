# -*- coding: utf-8 -*-
import scrapy
import logging

class ItcastSpider(scrapy.Spider):
    name = 'itcast'  # 爬虫名字 scrapy crawl itcast
    allowed_domains = ['itcast.cn']
    start_urls = ['http://www.itcast.cn/channel/teacher.shtml']

    def parse(self, response):  # response是start_url地址的响应
        # 实现数据的提取
        # t = response.xpath("//div[@class='tea_con']//h3/text()").extract()
        # print(t)
        logging.warning("_"*20)

        li_list = response.xpath("//div[@class='tea_con']//li")
        for li in li_list:
            item = {}
            item["name"] = li.xpath(".//h3/text()").extract_first()
            item["title"] = li.xpath(".//h4/text()").extract_first()
            item["profile"] = li.xpath(".//p/text()").extract_first()

            # print(item)
            yield item