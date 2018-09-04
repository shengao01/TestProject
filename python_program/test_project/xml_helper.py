#coding=utf-8

import os
from xml.dom.minidom import Document

json_dict = {
  "status": 0,
  "msg": "\u6210\u529f",
  "data": [
    {
      "plan_source": {
        "key": 2,
        "value": "\u5de5\u5177\u7bb1\u521b\u5efa"
      },
      "check_type": {
        "key": "11",
        "value": "\u5168\u90e8\u68c0\u67e5"
      },
      "end_date": 1519920000000,
      "published_standard": "",
      "updated_user_id": "5a8f687b67e92c31906c67e5",
      "history_problem": "",
      "org_code": "2134657",
      "create_time": 1519890533000,
      "created_user_id": "5a8f687b67e92c31906c67e5",
      "plan_inspector": "zsg",
      "_id": "5a97b06567e92c31906c7625",
      "plan_name": "plan_1",
      "start_date": 1519833600000,
      "unit": {
        "value": "stract1",
        "key": "5a97af4067e92c31906c7621"
      },
      "check_background": ""
    }
  ],
  "seq": "042b026328b711e8acce000c295ef7f9"
}


class readFileToXML(object):
    def __init__(self):
        # self.filepath = filepath                        # 完整路径
        # self._path = os.path.split(filepath)[0]         # 文件的路径
        # self._filename = os.path.split(filepath)[1]     # 文件的名称
        self._filename = 'plan_json'
        # self.DATA_XML = readFileToXML.json2XML(self)        # XML格式数据


    def json2XML(self):
        '''
        生成XML文档。
        '''
        doc = Document()  #创建DOM文档对象
        root = doc.createElement('root')                        # 创建根元素
        doc.appendChild(root)

        Platform = doc.createElement('Platform')                # 创建root下第一节点Platform
        # Platform.setAttribute("date", self.DATA_JSON["datetime"])        # **赋值时间
        root.appendChild(Platform)

        PlatformNum = doc.createElement('PlatformNum')          # 创建Platform第一节点PlatformNum
        PlatformNum.setAttribute("description", "数据中心监控平台编号，以便识别，*****************************")
        PlatformNum_title = doc.createTextNode("1872_ZABBIX")
        PlatformNum.appendChild(PlatformNum_title)
        Platform.appendChild(PlatformNum)

        Module = doc.createElement('Module')                    # 创建Platform第一节点Module
        Module.setAttribute("description", "模块编号")
        Module_title = doc.createTextNode("M1")
        Module.appendChild(Module_title)
        Platform.appendChild(Module)

        datas = doc.createElement('datas')                      # 创建root下第一节点datas
        root.appendChild(datas)

        for ip in json_dict["data"]:
            data = doc.createElement('data')
            # data.setAttribute("ciNum", "CI201702230001(被监控服务器的ID，预留字段)")
            data.setAttribute("datetime", json_dict["data"][0]["plan_source"])
            data.setAttribute("host", json_dict["data"][0]["check_type"])
            data.setAttribute("ip", json_dict["data"][0]["updated_user_id"])
            # data_title = doc.createTextNode("")     # 为了解决自闭合标签。
            # data.appendChild(data_title)            # 为了解决自闭合标签。
            datas.appendChild(data)
        return doc.toprettyxml(indent="")

def makeXML(data):
    f = open(json_dict+'.xml', 'w', encoding='utf-8')
    f.write(data)
    f.close()


# 实例化
TEST = readFileToXML()

# 在当前目录下生成XML文件
data = TEST.json2XML()
makeXML(data)
# 打印XML格式数据
print("XML格式：\n %s " % data)
