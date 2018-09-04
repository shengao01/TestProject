# -*- coding: utf-8 -*-
import scrapy


class TuoziSpider(scrapy.Spider):
    name = 'tuozi'
    allowed_domains = ['cl.koco.pw', 'sxeimg.com']

    start_urls = ['http://cl.koco.pw/htm_data/7/1712/2844537.html']

    def parse(self, response):
        img_list = response.xpath('//tr[@class="tr3"]/td/b/p/img/@src').extract()
        # span = response.xpath('//tr[@class="tr1 do_not_catch"]/th[2]/table//tr/td/div[4]/b/b/b/b/b//span/b/span')
        # img_list = span.xpath("./img/@src").extract()
        # title_list = span.xpath("./text()").extract()
        # nvs = zip(title_list,img_list)
        # item_dict = dict((title,img) for title,img in nvs)
        item = {}
        for url in img_list:
            print(url)
            item['href'] = url
            yield scrapy.Request(
                item['href'],
                callback=self.parse_img,
                meta={'item':item}
            )


    def parse_img(self, response):
        item = response.meta['item']
        # print(item['href'])
        # title = str(item['title'])+item['url'][-4:]
        title = item['url'][-10:]
        img_content = response.body
        file_path = 'tuozhi/' + title
        with open(file_path, 'wb') as f:
            f.write(img_content)
