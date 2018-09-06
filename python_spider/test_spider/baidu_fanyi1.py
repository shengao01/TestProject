import requests
import json


class Baidu_Fanyi():
    def __init__(self):
        self.url = "http://fanyi.baidu.com/v2transapi"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        }

    # 1.准备post的数据
    def prepare_data(self):
        user_input = input('请输入需要翻译的文字:')
        data = {
        "from":"zh",
        "to":"en",
        "query": user_input,
        "transtype": "translang",
        "simple_means_flag": "3"
        }

        return data

    # 2.发送请求,获取响应
    def parse_url(self, data, url):
        resp = requests.post(url, data=data, headers=self.headers)
        return resp.content.decode()

    # 3.提取数据返回响应结果
    def get_content(self, html_str):
        resp_dict = json.loads(html_str)
        res = resp_dict['trans_result']['data'][0]['dst']
        return res

    # 运行主逻辑
    def run(self):
        post_data = self.prepare_data()
        html_str = self.parse_url(post_data, self.url)
        dict = self.get_content(html_str)
        print(dict)


if __name__ == '__main__':
    fanyi = Baidu_Fanyi()
    fanyi.run()
