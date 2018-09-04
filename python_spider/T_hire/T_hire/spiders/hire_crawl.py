# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ..items import THireItem
import time

class HireCrawlSpider(CrawlSpider):
    name = 'hire_crawl'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?start=0']

    rules = (
        Rule(LinkExtractor(allow=r'position.php\?&start=\d+#a$'), callback='parse_item', follow=True),
    )

    # def start_requests(self):
    #     while True:
    #         time.sleep(2)
    #         yield scrapy.Request(
    #             self.start_urls[0],
    #             callback=self.parse_item,
    #             dont_filter=True
    #         )

    def parse_item(self, response):
        tr_list = response.xpath("//table[@class='tablelist']//tr[@class='even']")
        tr_list1 = response.xpath("//table[@class='tablelist']//tr[@class='odd']")
        for tr in tr_list1:
            tr_list.append(tr)
        tr_list = tr_list.extend(tr_list1)
        # print(tr_list)
        for tr in tr_list:
            item = THireItem()
            item['title'] = tr.xpath("./td[1]/a/text()").extract_first()
            item['type'] = tr.xpath("./td[2]/text()").extract_first()
            item['num'] = tr.xpath("./td[3]/text()").extract_first()
            item['addr'] = tr.xpath("./td[4]/text()").extract_first()
            item['pub_date'] = tr.xpath("./td[5]/text()").extract_first()
            print(item)
            yield item
