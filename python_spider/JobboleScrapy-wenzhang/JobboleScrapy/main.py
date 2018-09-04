# -*- coding: utf-8 -*-
import pymysql
pymysql.install_as_MySQLdb()
from scrapy.cmdline import execute
import sys
import os

# 打印main.py的路径
print(os.path.abspath(__file__))
# 通过main.py获取项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
# 执行scrapy脚本
execute(["scrapy","crawl","jobbole"])