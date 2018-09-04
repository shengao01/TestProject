# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy


class DetailSpider(scrapy.Spider):
    name = 'detail'
    allowed_domains = ['cl.hc5l.pw',
                       'sxotu.com', 'sximg.com', 'sxeimg.com', 'srimg.com', '69img.com', 'siimg.com', 'x6img.com',
                       'vxotu.com', 'tumblr.com', 'tu303.com',
                       's7tu.com', 's6tu.com', 's2tu.com',
                       '1024dmg.com', 'erooups.com', 'femjoyhunter.com', 'upload.vstanced.com',
                       'vstanced.com', 'hegrehunter.com', 'elitebabes.com', 'cdn1.babehub.com',
                       'postimg.org', 'cl.koco.pw', 'sinaimg.cn', 'poco.cn', 'wi.to', 'freeimage.us']

    start_urls = ['http://cl.hc5l.pw/htm_data/7/1802/3017549.html']

    def parse(self, response):
        item = {}
        img_list = response.xpath('//td/div//img/@src').extract()
        # span = response.xpath('//tr[@class="tr1 do_not_catch"]/th[2]/table//tr/td/div[4]/b/b/b/b/b//span/b/span')
        # img_list = span.xpath("./img/@src").extract()
        # title_list = span.xpath("./text()").extract()
        # nvs = zip(title_list,img_list)
        # item_dict = dict((title,img) for title,img in nvs)
        for url in img_list:
            print(url)
            item['href'] = url
            yield scrapy.Request(
                item['href'],
                callback=self.parse_img,
                meta={'item': deepcopy(item)}
            )

    def parse_img(self, response):
        # item = deepcopy(response.meta['item'])
        item = deepcopy(response.meta['item'])
        print(item['href'])
        # title = str(item['title'])+item['url'][-4:]
        title = item['href'][-10:]
        title = 'asiwa' + title
        if '/' in title:
            title = title.replace('/', 'a')
        if '\\' in title:
            title = title.replace('\\', 'a')
        if '_' in title:
            title = title.replace('_', 'a')
        img_content = response.body
        # file_path = 'eur/'+title
        # file_path = 'asia/'+title
        file_path = 'gif/' + title
        with open(file_path, 'wb') as f:
            f.write(img_content)
