# coding: utf-8

import requests
from bs4 import BeautifulSoup
from lxml import etree
import json


class BtcSpider(object):
    def __init__(self):
        self.url='http://8btc.com/forum-61-{}.html'
        self.headers={
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'}
        self.data_list=[]
        self.data_detail=[]

    # 1.发请求
    def get_response(self, url):
        response=requests.get(url, headers=self.headers)
        data=response.text
        # data = unicode(data, "gbk").encode("utf8")
        return data

    # 2.解析数据
    def parse_list_data(self, data):
        soup=BeautifulSoup(data, 'lxml')
        # 解析内容
        title_list=soup.select('.s')
        for title in title_list:
            list_dict_data={}
            list_dict_data['title']=title.get_text().strip().replace('\r', '').replace('\n', '')
            list_dict_data['detail_url']=title.get('href')
            print(list_dict_data)
            self.data_list.append(list_dict_data)

    #  解析详情页
    def parse_detail_data(self, data):
        html_data=BeautifulSoup(data, 'lxml')
        # 取出问题
        question=html_data.select('#thread_subject')[0].get_text()

        answer_list=html_data.select('.t_f')

        for answer in answer_list:
            answer_list=[]
            answer_list.append(answer.get_text().strip().replace('\r', '').replace('\n', '').replace('\xa0', ''))
            detail_data={
                "question": question,
                "answer": answer_list
            }
            self.data_detail.append(detail_data)

    # 3.保存数据
    def save_data(self, data, file_path):
        data_str=str(data)
        data_str = data_str.encode('gbk').decode('utf-8')
        print(data_str)
        with open(file_path, 'w+') as f:
            f.write(data_str)

    def start(self):
        # ：列表页的请求
        for i in range(1, 3):
            url=self.url.format(i)
            data=self.get_response(url)
            self.parse_list_data(data)
            self.save_data(self.data_list, '077list.json')

        # 发送分详情页的请求
        for data in self.data_list:
            detail_url=data['detail_url']
            detail_data=self.get_response(detail_url)
            self.parse_detail_data(detail_data)
            self.save_data(self.data_detail, 'detail.json')


BtcSpider().start()
