import requests


# 采用面向对象的方式写代码
# 使用到了格式化字符串以及类方法之间进行传参的技巧
# http://tieba.baidu.com/f?kw=%E5%90%88%E8%82%A5%E5%B7%A5%E4%B8%9A%E5%A4%A7%E5%AD%A6&ie=utf-8&pn=50
class TiebaSpider():
    # 初始化
    def __init__(self, name):
        self.name = name
        self.url_list = "http://tieba.baidu.com/f?kw=" + self.name + "&ie=utf-8&pn={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}

    # 获取url列表
    def get_urllist(self):
        urlList = [self.url_list.format(i * 50) for i in range(0, 2)]
        # print(urlList)
        return urlList

    # 解析url,发送请求,获取响应
    def parse_url(self, url):
        # print(url)
        html_str = requests.get(url, headers=self.headers, timeout=10)
        return html_str.content

    # 保存html字符串
    def save_html(self, html_str, page_num):
        file_path = "{}_第{}页的内容.html".format(self.name, page_num)
        with open(file_path, 'wb') as f:
            f.write(html_str)

    # 运行主函数
    def run(self):
        urlList = self.get_urllist()
        for url in urlList:
            print(url)
            html_str = self.parse_url(url)
            page_num = urlList.index(url) + 1
            self.save_html(html_str, page_num)


if __name__ == '__main__':
    kw = input('请输入要爬取的贴吧名:')
    tieba = TiebaSpider(kw)
    # tieba = TiebaSpider("合肥工业大学")
    tieba.run()
