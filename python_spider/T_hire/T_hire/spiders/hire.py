# -*- coding: utf-8 -*-
import scrapy
from ..items import THireItem
import time

class HireSpider(scrapy.Spider):
    name = 'hire'
    allowed_domains = ['hr.tencent.com']
    start_urls = ['http://hr.tencent.com/position.php?start=0']

    def start_requests(self):
        while True:
            time.sleep(2)
            yield scrapy.Request(self.start_urls[0], callback=self.parse, dont_filter=True)

    def parse(self, response):
        print(response.request.headers['User-Agent'])
        print('*'*50)



    # def parse(self, response):
    #     tr_list = response.xpath("//table[@class='tablelist']//tr[@class='even']")
    #     tr_list1 = response.xpath("//table[@class='tablelist']//tr[@class='odd']")
    #     for tr in tr_list1:
    #         tr_list.append(tr)
    #     # tr_list = tr_list.extend(tr_list1)
    #     # print(tr_list)
    #     for tr in tr_list:
    #         item = THireItem()
    #         item['title'] = tr.xpath("./td[1]/a/text()").extract_first()
    #         item['type'] = tr.xpath("./td[2]/text()").extract_first()
    #         item['num'] = tr.xpath("./td[3]/text()").extract_first()
    #         item['addr'] = tr.xpath("./td[4]/text()").extract_first()
    #         item['pub_date'] = tr.xpath("./td[5]/text()").extract_first()
    #         print(item)
    #         yield item
    #
    #     # 获取下一页
    #     next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
    #     next_url = "http://hr.tencent.com/"+next_url
    #     yield scrapy.Request(
    #         next_url,
    #         callback=self.parse
    #     )

