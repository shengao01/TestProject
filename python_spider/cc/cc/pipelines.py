# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class CcPipeline(object):
    def process_item(self, item, spider):
        file_path = 'xiezhen/'+item['title']
        with open(file_path,'wb') as f:
            f.write(item['img_content'])
