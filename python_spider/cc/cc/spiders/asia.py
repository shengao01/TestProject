# -*- coding: utf-8 -*-
import scrapy
from copy import deepcopy

class AsiaSpider(scrapy.Spider):
    name = 'asia'
    allowed_domains = ['cc.o8d.win',
                       'sxotu.com', 'sximg.com', 'sxeimg.com', 'srimg.com', '69img.com', 'siimg.com', 'x6img.com',
                       'vxotu.com', 'tumblr.com', 'tu303.com',
                       's7tu.com', 's6tu.com', 's2tu.com',
                       '1024dmg.com', 'erooups.com', 'femjoyhunter.com', 'upload.vstanced.com',
                       'vstanced.com', 'hegrehunter.com', 'elitebabes.com', 'cdn1.babehub.com',
                       'postimg.org', 'cl.koco.pw', 'sinaimg.cn', 'poco.cn', 'wi.to', 'freeimage.us']
    # start_urls = ['http://cl.hc5l.pw/thread0806.php?fid=8&type=1']
    # start_urls = ['http://cl.hc5l.pw/thread0806.php?fid=16']
    type = 7
    start_urls = ['https://cc.o8d.win/thread0806.php?fid={}'.format(type)]

    def parse(self, response):
        tr_list = response.xpath("//tr[@class='tr3 t_one tac']")
        for tr in tr_list:
            item = {}
            href_list = tr.xpath("./td[2]/h3/a/@href").extract()
            for href in href_list:
                item['href'] = "https://cc.o8d.win/" + href
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
            next_url = "https://cc.o8d.win/" + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse,
            )

    def parse_detail(self, response):
        print("enter.......................")
        item = deepcopy(response.meta['item'])

        # item['head'] = response.xpath("//div[@class='category-title']/h2/text()").extract()
        # 一般
        # img_href_list = response.xpath("//div[@class='tpc_content do_not_catch']//input/@src").extract()
        # 技术讨论区
        img_href_list = response.xpath("//div[@class='tpc_content do_not_catch']//img/@src").extract()

        # yield item
        for img_href in img_href_list:
            print(img_href)
            item['img_href'] = img_href
            yield scrapy.Request(
                img_href,
                callback=self.parse_img,
                meta={"item": deepcopy(item)}
            )

    def parse_img(self, response):
        item = deepcopy(response.meta['item'])
        title = item['img_href'][-10:]
        if '/' in title:
            title = title.replace('/', 'a')
        if '\\' in title:
            title = title.replace('\\', 'a')
        if '_' in title:
            title = title.replace('_', 'a')
        img_content = response.body
        # file_path = 'eur/'+title
        # file_path = 'asia/'+title
        file_path = 'tec1/'+title
        with open(file_path, 'wb') as f:
            f.write(img_content)

    # def parse_img(self, response):
    #     item = deepcopy(response.meta['item'])
    #     item['title'] = item['img_href'][-10:]
    #     item['img_content'] = response.body
    #     yield item
