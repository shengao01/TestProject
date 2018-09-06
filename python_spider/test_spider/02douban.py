import requests
import json

class DouBanTV():
    def __init__(self):
        self.url_temp_list = [
            {
                "url": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_american_hot/items?os=ios&for_mobile=1&start={}&count=18&loc_id=108288",
                "country": "US"
            },
            {
                "url": "https://m.douban.com/rexxar/api/v2/subject_collection/filter_tv_domestic_hot/items?os=ios&for_mobile=1&start={}&count=18&loc_id=108288",
                "country": "CN"
            }
        ]
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"}
        with open("douban_tv.csv", "a", encoding="GBK") as f:
            f.write("标题,演员,导演,评分人数,评分"+"\n")

    def parse_url(self, url):
        print(url)
        response = requests.get(url, headers=self.headers, timeout=5)
        return response.content.decode()

    def get_content_list(self, json_response):  # 提取数据
        dict_response = json.loads(json_response)
        content_list = dict_response['subject_collection_items']
        total = dict_response["total"]
        return content_list, total

    def save_content_list(self, content_list, country):  # 保存数据
        with open("douban_tv.csv", "a", encoding="GBK") as f:
            for content in content_list:
                content["country"] = country
                temp_list = [content["title"], "/".join(content["actors"]), "/".join(content["directors"]),
                             content["rating"]["count"], content["rating"]["value"]]
                temp_str = ",".join([str(i) for i in temp_list]) + "\n"
                f.write(temp_str)

    def run(self):  # 实现主要逻辑
        for url_temp in self.url_temp_list:
            # 1.start_url 给定初始的url
            num = 0
            total = 100
            while num < total + 18:  # 假设最后还有10条数据没有取到，num+18会大于 total
                url = url_temp["url"].format(num)
                # 2.发送请求，获取响应
                json_response = self.parse_url(url)
                # 3.提取数据
                content_list, total = self.get_content_list(json_response)
                # 4.保存
                self.save_content_list(content_list, url_temp["country"])
                # 5.构造下一页的URL地址，进入循环
                num += 18

if __name__ == '__main__':
    douban = DouBanTV()
    douban.run()
