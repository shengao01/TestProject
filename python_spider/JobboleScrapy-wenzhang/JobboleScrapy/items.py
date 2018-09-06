# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
import time

class JobbolescrapyItem(scrapy.Item):
    title = scrapy.Field()
    public_date = scrapy.Field()
    article_url = scrapy.Field()
    article_img_url = scrapy.Field()
    tags = scrapy.Field()
    comment_nums = scrapy.Field()
    # created_at = scrapy.Field()
    content = scrapy.Field()

    def get_article_info_insert_sql(self):
        insert_sql = """
            insert into all_posts(
            title,
            public_date,
            article_url,
            article_img_url,
            tags,
            comment_nums,
            created_at,
            content
            )
            values(%s, %s, %s, %s, %s, %s, %s, %s)  
        """
        # ; ON DUPLICATE KEY UPDATE created_at = unix_timestamp(now()) 
        #DATE_FORMAT(NOW(),'%Y/%m/%d')

        params = (self['title'],
                  self['public_date'],
                  self['article_url'],
                  self['article_img_url'],
                  self['tags'],
                  self['comment_nums'],
                  int(time.time()),
                  self['content'])


        return insert_sql, params


       


