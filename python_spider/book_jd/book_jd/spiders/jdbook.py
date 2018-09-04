# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy


class JdbookSpider(scrapy.Spider):
    name = 'jdbook'
    allowed_domains = ['jd.com']
    start_urls = ['http://book.jd.com/booksort.html']

    def parse(self, response):
        dt_list = response.xpath("//div[@class='w main']//dl/dt")
        for dt in dt_list:
            item = {}
            item['b_cate'] = dt.xpath("./a/text()").extract_first()
            # item['b_href'] = dt.xpath("./a/@href").extract_first()
            em_list = dt.xpath("./following-sibling::*[1]/em")
            for em in em_list:
                item['s_cate'] = em.xpath("./a/text()").extract_first()
                item['s_href'] = em.xpath("./a/@href").extract_first()
                if item['s_href'] is not None:
                    item['s_href'] = 'http:' + item['s_href']
                    yield scrapy.Request(
                        item['s_href'],
                        callback=self.parse_book_list,
                        meta={'item': deepcopy(item)}
                        # meta={'item':item}
                    )

    def parse_book_list(self, response):
        item = response.meta['item']
        li_list = response.xpath("//div[@class='m-list']//ul[@class='gl-warp clearfix']/li")
        for li in li_list:
            item['book_name'] = li.xpath(".//div[@class='p-name']/a/em/text()").extract_first()
            item['book_href'] = li.xpath(".//div[@class='p-name']/a/@href").extract_first()
            item['book_img'] = li.xpath(".//div[@class='p-img']/a/@href").extract_first()
            if item['book_img'] is not None:
                item['book_img'] = 'http:'+item['book_img']

        # 获取翻页数据
        next_url = response.xpath("//a[@class='pn-next']/@href").extract_first()
        if next_url is not None:
            next_url = 'http://list.jd.com'+next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse_book_list
            )
        print(item)

