# -*- coding: utf-8 -*-
import scrapy


class XianduSpider(scrapy.Spider):
    name = 'xiandu'
    allowed_domains = ['gank.io']
    start_urls = ['http://gank.io/xiandu']

    def parse(self, response):
        li_list = response.xpath("//div[@class='xiandu_choice']/ul//li")
        for li in li_list:
            item = {}
            # item['index'] = li.xpath("./div[1]/span[1]/text()").extract_first()
            # item['title'] = li.xpath("./div[1]/a/text()").extract_first()
            item['href'] = li.xpath("./a/@href").extract_first()
            item['href'] = 'http://gank.io' + item['href']
            item['head'] = li.xpath("./a/img/@title").extract_first()
            print("-->"*10,item)
            # 获取详情页
            yield scrapy.Request(
                item["href"],
                callback=self.parse_list,
                meta={"item": item}
            )

    def parse_list(self, response):
        item = response.meta['item']
