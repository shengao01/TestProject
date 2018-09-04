# -*- coding: utf-8 -*-
import re
# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class AzufangPipeline(object):
    def process_item(self, item, spider):
        item['title'] = item['title'].strip()
        if ',' in item['title']:
            item['title'] = re.sub(',','',item['title'])
        if ',' in item['area_detail']:
            item['area_detail'] = re.sub(',','',item['area_detail'])
        item['huxing'] = item['desc'][0:6]
        item['square'] = item['desc'][-7:].strip()
        print(item)
        with open('whzf58.csv','a') as f:
            temp_list = [item['title'],item['area'],item['area_detail'],item['huxing'],item['square'],item['price'],item['href']]
            temp_str = ','.join(temp_list)
            f.write(temp_str+'\n')


class QfangPipeline(object):
    def process_item(self, item, spider):
        if ',' in item['title']:
            item['title'] = re.sub(',','',item['title'])

        item['area'] = ''.join(item['desc'][0:2])
        item['area'] = item['area'][0:-2]
        item['area_detail'] = item['desc'][2]
        item['square'] = re.sub('平米','㎡',item['square'])

        print(item)
        with open('zfqfang.csv','a') as f:
            temp_list = [item['title'],item['area'],item['area_detail'],item['huxing'],item['square'],item['price'],item['href']]
            temp_str = ','.join(temp_list)
            f.write(temp_str+'\n')