# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
with open('tencent_hire.csv','a', encoding='utf-8') as f:
    f.write("职位名称,职位类别,人数,地点,发布时间"+"\n")


class THirePipeline(object):
    def process_item(self, item, spider):
        with open('tencent_hire.csv','a', encoding='utf-8') as f:
            temp_list = [item['title'], item['type'], item['num'], item['addr'], item['pub_date']]
            temp_str = ",".join([str(i) for i in temp_list])
            f.write(temp_str+"\n")
