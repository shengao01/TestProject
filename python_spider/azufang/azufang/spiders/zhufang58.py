# -*- coding: utf-8 -*-
import scrapy


class Zhufang58Spider(scrapy.Spider):
    name = 'zhufang58'
    allowed_domains = ['58.com']
    start_urls = ['http://58.com/']

    with open('houssp58.csv', 'a') as f:
        f.write('标题,区域1,区域2,户型,面积,价格,房屋链接'+'\n')

    def parse(self, response):
        li_list = response.xpath('//div/ul[@class="listUl"]/li')[:-1]
        for li in li_list:
            item = {}
            item['title'] = li.xpath("./div[2]/h2/a/text()").extract_first()
            item['price'] = li.xpath("./div[3]/div[2]/b/text()").extract_first()
            item['area'] = li.xpath("./div[2]/p[2]/a[1]/text()").extract_first()
            # item['square'] = li.xpath("./div[2]/h2/a/text()").extract_first()
            item['area_detail'] = li.xpath("./div[2]/p[2]/a[2]/text()").extract_first()
            item['desc'] = li.xpath("./div[2]/p[1]/text()").extract_first()
            item['href'] = li.xpath("./div[1]/a/@href").extract_first()
            # print(item['href'])

            # yield scrapy.Request(
            #     item['href'],
            #     callback=self.parse_img,
            #     meta={'item': deepcopy(item)}
            # )
            # print(item)
            yield item

        # 获取下一页
        next_url = response.xpath('.//a[@class="next"]/@href').extract_first()
        print(next_url)
        # time.sleep(1)
        # print(next_url+'#'*20)
        yield scrapy.Request(
            next_url,
            callback=self.parse
        )
