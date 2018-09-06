# -*- coding: utf-8 -*-
import scrapy
import re

class Github2Spider(scrapy.Spider):
    name = 'github2'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/login']

    def parse(self, response):
        yield scrapy.FormRequest.from_response(
            response,
            callback = self.after_login,
            formdata={
                'login':'401491197@qq.com',
                'password':'zsg@19941014'
            },
        )

    def after_login(self, response):
        print(re.findall(r'shengao01', response.body.decode()))
