# -*- coding: utf-8 -*-
import scrapy


class TempSpider(scrapy.Spider):
    name = 'temp'
    allowed_domains = ['gank.io','solidot.org','www.qdaily.com' ]
    start_urls = ['http://gank.io/xiandu/view/qdaily']

    def parse(self, response):
        div_list = response.xpath("//div[@class='xiandu_items']/div[@class='xiandu_item']")
        for div in div_list:
            item = {}
            item['index'] = div.xpath("./div[1]/span[1]/text()").extract_first()
            item['title'] = div.xpath("./div[1]/a/text()").extract_first()
            item['href'] = div.xpath("./div[1]/a/@href").extract_first()
            item['src'] = div.xpath("./div[2]/a/@title").extract_first()
            # print("-->"*10,item)
            # 获取详情页
            yield scrapy.Request(
                item["href"],
                callback=self.parse_detail,
                meta={"item": item}
            )

        # 获取下一页
        next_url = response.xpath("//a[text()='下一页']/@href").extract_first()
        if next_url is not None:
            next_url = "http://gank.io"+next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )

    def parse_detail(self, response):
        print("enter.......................")
        item = response.meta['item']
        if item['src'] == '好奇心日报':
            # item['head'] = response.xpath("//div[@class='category-title']/h2/text()").extract()
            item['content'] = response.xpath("//div/div[@class='detail']/p/text()").extract()
            # item['detail'] = response.xpath("//div/div[@class='detail']/p/b/text()").extract()
            item['img_href'] = response.xpath("//div/div[@class='detail']/div/figure/img/@src").extract()
        # yield item
        print(item)