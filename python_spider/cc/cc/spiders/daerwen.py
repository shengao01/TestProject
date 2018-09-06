# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy

class DaerwenSpider(scrapy.Spider):
    name = 'daerwen'
    allowed_domains = ['p.vxotu.com','cl.koco.pw','www.srimg.com','www1.wi.to','s2tu.com','//www.sxotu.com','41.media.tumblr.com','36.media.tumblr.com','40.media.tumblr.com','s7tu.com','www.s2tu.com','www.s6tu.com', 'www.1024dmg.com','tu303.com','www.sxotu.com','www1.wi.to','img181.poco.cn','upload.vstanced.com','www.srimg.com','www.69img.com', 'content.erooups.com', 'cdn1.femjoyhunter.com', 's7tu.com',
                        'www.sxeimg.com']
    start_urls = ['http://cl.koco.pw/thread0806.php?fid=16']

    def parse(self, response):
        tr_list = response.xpath("//tr[@class='tr3 t_one tac']")
        for tr in tr_list:
            item = {}
            href_list = tr.xpath("./td[2]/h3/a/@href").extract()
            for href in href_list:
                item['href'] = "http://cl.koco.pw/"+href
                # item['src'] = div.xpath("./div[2]/a/@title").extract_first()
                # print(item)
                # 获取详情页
                yield scrapy.Request(
                    item["href"],
                    callback=self.parse_detail,
                    meta={"item": deepcopy(item)}
                )

        # 获取下一页
        next_url = response.xpath("//a[text()='下一頁']/@href").extract_first()
        if next_url is not None:
            next_url = "http://cl.koco.pw/"+next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )

    def parse_detail(self, response):
        print("enter.......................")
        item = deepcopy(response.meta['item'])

        # item['head'] = response.xpath("//div[@class='category-title']/h2/text()").extract()
        img_href_list = response.xpath("//div[@class='tpc_content do_not_catch']//input/@src").extract()

        # yield item
        for img_href in img_href_list:
            print(img_href)
            item['img_href'] = img_href
            yield scrapy.Request(
                img_href,
                callback=self.parse_img,
                meta={"item": deepcopy(item)}
            )

    # def parse_img(self, response):
    #     item = deepcopy(response.meta['item'])
    #     title = item['img_href'][-10:]
    #     img_content = response.body
    #     file_path = 'photo1/'+title
    #     with open(file_path,'wb') as f:
    #         f.write(img_content)

    def parse_img(self, response):
        item = deepcopy(response.meta['item'])
        item['title'] = item['img_href'][-10:]
        item['img_content'] = response.body
        yield item
