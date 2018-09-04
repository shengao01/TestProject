# -*- coding: utf-8 -*-
import xml_helper as RFTX

# 实例化
TEST = RFTX.readFileToXML("plan.json")
#TEST = RFTX.readFileToXML("C:\\Users\\Asktao\\PycharmProjects\\CSV_to_XML\\zmonitor.2017-04-06-14_28")

# 在当前目录下生成XML文件
TEST.makeXML()

# 打印XML格式数据
print("XML格式：\n %s " % TEST.DATA_XML)

print(TEST._path)       # 路径
print(TEST._filename)   # 文件名