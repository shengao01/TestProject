import requests
import re
from lxml import etree
from queue import Queue
# from retrying import retry


class TiebaSpider():
    def __init__(self, name):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 9_1 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Version/9.0 Mobile/13B143 Safari/601.1"
        }
        self.start_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/m?kw={}".format(name)
        self.part_url = "http://tieba.baidu.com/mo/q----,sz@320_240-1-3---2/"
        self.name = name

        self.url_queue = Queue()
        self.html_str_queue = Queue()
        self.content_list_queue = Queue()

    def _parse_url(self, url):
        # 发送请求,获取响应
        resp = requests.get(url, headers=self.headers, timeout=5)
        return resp.content

    def parse_url(self, url):
        print(url)
        try:
            html_str = self._parse_url(url)
        except:
            html_str = None

        # print('after parse url')
        return html_str

    def get_img_list(self, detail_url, total_img_list):
        # 4.请求帖子的地址
        # 5.提取帖子详情页的图片地址，下一页的url地址
        if detail_url is not None:
            detail_html_str = self.parse_url(detail_url)
            detail_html = etree.HTML(detail_html_str)
            img_list = detail_html.xpath("//img[@class='BDE_Image']/@src")
            total_img_list += img_list
            # 6.请求下一页的URL地址，循环4-6步，详情页么有下一页结束
            next_datail_url = detail_html.xpath("//a[text()='下一页']/@href")
            if len(next_datail_url) > 0:
                next_detail_url = self.part_url + next_datail_url[0]
                return self.get_img_list(next_detail_url, total_img_list)
            else:
                return total_img_list
        else:
            return total_img_list

    def get_content_list(self, html_str):
        # print('before get content list')
        html = etree.HTML(html_str)
        # print('after etree')
        # 获取页面当中的div标签
        # div_list = html.xpath("//body/div/div[@class='i']")
        div_list = html.xpath("//body/div/div[contains(@class,'i')]")
        # print(div_list)
        content_list = []
        # 3.从列表页提取数据，帖子地址，帖子标题，下一页的url地址
        for div in div_list:
            item = {}
            item["title"] = div.xpath("./a/text()")[0] if len(div.xpath("./a/text()")) > 0 else None
            item["href"] = self.part_url + div.xpath("./a/@href")[0] if len(div.xpath("./a/@href")) > 0 else None
            item["img_list"] = self.get_img_list(item["href"], [])
            # http://c.hiphotos.baidu.com/forum/w%3D400%3Bq%3D80%3Bg%3D0/sign=c8670d2a9cdda144da096db2828ca19f/0d83902397dda1446984c58bb9b7d0a20df486ca.jpg?&src=http%3A%2F%2Fimgsrc.baidu.com%2Fforum%2Fpic%2Fitem%2F0d83902397dda1446984c58bb9b7d0a20df486ca.jpg
            # 解码大图
            item["img_list"] = [requests.utils.unquote(i).split("&src=")[-1] for i in item["img_list"]]
            # print(item["img_list"])
            content_list.append(item)
        # 提取下一页的url地址
        next_url = html.xpath("//a[text()='下一页']/@href")
        if len(next_url) > 0:
            next_url = self.part_url + next_url[0]
        else:
            next_url = None

        return content_list, next_url

    def save_content_list(self, content_list):
        with open("tieba.csv","a", encoding="utf-8") as t:
            for content in content_list:
                temp_list = [content["title"],content["href"]]
                temp_str = ",".join([str(i) for i in temp_list])
                t.write(temp_str)
                for img_url in content["img_list"]:
                    img_title = "内涵图/"+img_url[-10:]
                    img_cont = self.parse_url(img_url)
                    with open(img_title,'wb') as f:
                        f.write(img_cont)

    def run(self):
        # 1.start_url
        next_url = self.start_url
        while next_url is not None:
            # 2.获取第一页的列表页的页面内容
            html_str = self.parse_url(next_url)
            # 3.从列表页提取数据，帖子地址，帖子标题，下一页的url地址
            # 4.请求帖子的地址
            # 5.提取帖子详情页的图片地址，下一页的url地址
            # 6.请求下一页的URL地址，循环4-6步，详情页么有下一页结束
            content_list, next_url = self.get_content_list(html_str)
            # print(content_list)
            self.save_content_list(content_list)
            # 7.请求列表页的下一页，进入循环2-7步，列表页没有下一页的时候结束


if __name__ == '__main__':
    t_s = TiebaSpider('')
    t_s.run()
