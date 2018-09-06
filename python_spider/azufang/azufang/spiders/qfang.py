# -*- coding: utf-8 -*-
import scrapy


class QfangSpider(scrapy.Spider):
    name = 'qfang'
    allowed_domains = ['qfang.com']
    start_urls = ['http://shenzhen.qfang.com/rent']
    with open('zfqfang.csv', 'a') as f:
        f.write('标题,区域1,区域2,户型,面积,价格,房屋链接'+'\n')

    def parse(self, response):
        li_list = response.xpath('//div[@class="house-detail"]/ul/li')
        for li in li_list:
            item = {}
            item['title'] = li.xpath("./div[1]/p/a/text()").extract_first()
            item['price'] = li.xpath("./div[2]/span[1]/text()").extract_first()
            item['desc'] = li.xpath("./div[1]/p[3]/span[2]/a/text()").extract()
            # item['square'] = li.xpath("./div[2]/h2/a/text()").extract_first()
            # item['area_detail'] = li.xpath("./div[2]/p[2]/a[2]/text()").extract_first()
            item['huxing'] = li.xpath("./div[1]/p[2]/span[2]/text()").extract_first()
            item['square'] = li.xpath("./div[1]/p[2]/span[4]/text()").extract_first()
            item['href'] = li.xpath("./a/@href").extract_first()
            item['href'] = 'http://shenzhen.qfang.com'+item['href']
            print(item)
            yield item

        # 获取下一页
        next_url = response.xpath("//a[@class='turnpage_next']/@href").extract_first()
        next_url = 'http://shenzhen.qfang.com'+next_url
        yield scrapy.Request(
            next_url,
            callback=self.parse
        )


        # //a[@class='turnpage_next']/@href
