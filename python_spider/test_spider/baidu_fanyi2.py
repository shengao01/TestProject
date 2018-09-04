import requests
import json
import sys


class Baidu_Fanyi():
    def __init__(self):
        self.url1 = "http://fanyi.baidu.com/langdetect"
        self.url = "http://fanyi.baidu.com/v2transapi"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        }

    # 1.通过第一步请求,获取语言类型
    # 1.1 获取要翻译的文字,准备发送请求,判断语言
    def prepare_data1(self):
        # self.user_input = sys.argv[1]
        self.user_input = input('请输入需要翻译的文字:')
        data = {
            "query": self.user_input
        }
        return data

    # 1.2发送请求,获取响应
    def parse_url1(self, data, url):
        resp = requests.post(url, data=data, headers=self.headers)
        return resp.content.decode()
        # resp = {"error":0,"msg":"success","lan":"zh"}

    # 1.3根据获取到的语言类别进行判别翻译方式
    def get_content1(self, html_str):
        resp_dict = json.loads(html_str)
        # print(resp_dict)
        lang = resp_dict['lan']
        return lang  # 为'zh' 或'en'

    # 2.执行翻译过程
    # 2.1准备post的数据
    def prepare_data(self, langStyle):
        data = {
            "from": "en",
            "to": "zh",
            "query": self.user_input,
            "transtype": "translang",
            "simple_means_flag": "3"
        }
        if langStyle == 'zh':
            data["from"] = "zh"
            data["to"] = "en"

        return data

    # 2.2发送请求,获取响应
    def parse_url(self, data, url):
        resp = requests.post(url, data=data, headers=self.headers)
        return resp.content.decode()

    # 2.3提取数据返回响应结果
    def get_content(self, html_str):
        resp_dict = json.loads(html_str)
        res = resp_dict['trans_result']['data'][0]['dst']
        return res

    # 运行主逻辑
    def run(self):
        try:
            post_data = self.prepare_data1()
            if post_data:
                html_str = self.parse_url1(post_data, self.url1)
                dict = self.get_content1(html_str)

                data = self.prepare_data(dict)
                resp = self.parse_url(data, self.url)
                res = self.get_content(resp)
                res = self.user_input + '   翻译的结果是:   ' + res
                print(res)
            else:
                print('不能为空')
                return False
        except Exception as e:
            raise e


if __name__ == '__main__':
    fanyi = Baidu_Fanyi()
    while True:
        fanyi.run()
