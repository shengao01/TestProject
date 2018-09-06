import requests
import re
from lxml import etree


class WangyiSpider():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        }
        self.part_url = "http://music.163.com"
        self.url_temp = "http://music.163.com/discover/playlist/?order=hot&cat=%E5%85%A8%E9%83%A8&limit=35&offset={}"
        with open("list.csv", "a", encoding="utf-8") as f:
            f.write("Title" + "\n")

    def get_url_list(self):
        url_list = [self.url_temp.format(i * 35) for i in range(0, 38)]
        return url_list

    def _parse_url(self, url):
        # 发送请求,获取响应
        resp = requests.get(url, headers=self.headers, timeout=5)
        return resp.content.decode()

    # 解析url获取页面内容的字符串
    def parse_url(self, url):
        try:
            html_str = self._parse_url(url)
        except:
            html_str = None
        return html_str

    # def get_img_list(self, detail_url, total_img_list):
    #     # 4.请求帖子的地址
    #     # 5.提取帖子详情页的图片地址，下一页的url地址
    #     if detail_url is not None:
    #         detail_html_str = self.parse_url(detail_url)
    #         detail_html = etree.HTML(detail_html_str)
    #         img_list = detail_html.xpath("//img[@class='BDE_Image']/@src")
    #         total_img_list += img_list
    #         # 6.请求下一页的URL地址，循环4-6步，详情页么有下一页结束
    #         next_datail_url = detail_html.xpath("//a[text()='下一页']/@href")
    #         if len(next_datail_url) > 0:
    #             next_detail_url = self.part_url + next_datail_url[0]
    #             return self.get_img_list(next_detail_url, total_img_list)
    #         else:
    #             return total_img_list
    #     else:
    #         return total_img_list

    # 获取歌单标题及每个歌单的完整链接

    def get_content_list(self, html_str):
        # <a title="十一月 | 电音鉴赏指南⚡️Top100" href="/playlist?id=1995337890" class="msk"></a>
        # pattern = re.compile(r'<a title="(.*?)" class="tit s-fc0" href="(.*?)" title')
        pattern = re.compile(r'<a title="(.*?)" href="(.*?)" class="msk"></a>')
        div_list = pattern.findall(html_str)
        print(str(div_list))
        content_list = []
        for div in div_list:
            item = {}
            item["title"] = div[0]
            item["href"] = self.part_url + div[1]
            content_list.append(item)
        return content_list

    # 通过歌单地址读取页面,并提取歌曲信息
    def get_song_list(self, url):
        html = self.parse_url(url)
        pattern = re.compile(r'<li><a href="/song\?id=\d+">(.*?)</a>')
        song_list = pattern.findall(html)
        return song_list

    # 保存歌单信息到表格中
    def save_song_list(self, list, a):
        with open("list.csv", "a", encoding="utf-8") as f:
            temp_str = ",".join([str(i) for i in list])
            f.write(a + temp_str + "\n")

    def run(self):
        url_list = self.get_url_list()
        for url in url_list:
            html_str = self.parse_url(url)
            content_list = self.get_content_list(html_str)

            for i in content_list:
                url = i['href']
                song_list = self.get_song_list(url)
                self.save_song_list(song_list, i["title"])


if __name__ == '__main__':
    t_s = WangyiSpider()
    t_s.run()
