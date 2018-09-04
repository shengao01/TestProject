# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
import MySQLdb.cursors
from twisted.enterprise import adbapi
import time


class JobbolescrapyPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        dbparams = dict(
            host = settings['MYSQL_HOST'],
            user = settings['MYSQL_USER'],
            password = settings['MYSQL_PASSWORD'],
            db = settings['MYSQL_DBNAME'],
            charset = 'utf8',
            cursorclass = MySQLdb.cursors.DictCursor,
            use_unicode = True
        )
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparams)
        return cls(dbpool)

    def process_item(self, item, spider):
        query_article = self.dbpool.runInteraction(self.do_insert_article_info, item)


        query_article.addErrback(self.handle_error, item, spider)

    def handle_error(self, failure, item, spider):
        print(failure)
        import codecs
        fw = codecs.open('jobbole_errLog.txt', 'a+', 'utf-8')
        fw.write(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + "\r\n" + str(failure))
        fw.close()

    def do_insert_article_info(self, cursor, item):
        insert_sql, params = item.get_article_info_insert_sql()

        try:
            # print(insert_sql % params,'*'*50)
            cursor.execute(insert_sql, params)
        except Exception as e:
            print(e)
        pass
        # else:
        #     print('-'*100)
