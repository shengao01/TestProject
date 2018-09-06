# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class AzufangItem(scrapy.Item):
    # define the fields for your item here like:
    price = scrapy.Field()
    area = scrapy.Field()
    square = scrapy.Field()
    desc = scrapy.Field()
    title = scrapy.Field()
    area_detail = scrapy.Field()
    huxing = scrapy.Field()
    img_href = scrapy.Field()
    href = scrapy.Field()

