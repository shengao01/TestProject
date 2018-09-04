# -*- coding: utf-8 -*-
import scrapy


class LeleSpider(scrapy.Spider):
    name = 'lele'
    allowed_domains = ['lele.com']
    start_urls = ['http://lele.com/']

    def parse(self, response):
        pass
