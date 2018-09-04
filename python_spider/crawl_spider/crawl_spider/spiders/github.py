# -*- coding: utf-8 -*-
import scrapy
import re

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']
    start_urls = ['http://github.com/login']

    def parse(self, response):
        authenticity_token = response.xpath("//input[@name='authenticity_token']/@value").extract_first()
        form_data = {
            'commit': 'Sign in',
            'utf8':'✓',
            'authenticity_token':authenticity_token,
            'login': '401491197@qq.com',
            'password': 'zsg@19941014'
        }

        yield scrapy.FormRequest(
            'http://github.com/session',
            callback=self.after_login,
            formdata=form_data
        )

    def after_login(self, response):
        print(re.findall(r'shengao01',response.body.decode()))