# coding=utf-8
import requests
# from retrying import retry
from lxml import etree
import json
import threading
from queue import Queue


class QiubaiSpider:
    def __init__(self):
        self.url_temp = "https://www.qiushibaike.com/8hr/page/{}/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"}
        self.url_queue = Queue()
        self.html_str_queue = Queue()
        self.content_list_queue = Queue()
        with open("qiubai.csv", "a", encoding='utf-8') as f:
            f.write("作者,内容,点赞数 ,图片链接"+"\n")

    def get_url_list(self):
        # url_list = [self.url_temp.format(i) for i in range(1, 14)]
        # return url_list
        for i in range(14):
            self.url_queue.put(self.url_temp.format(i))

    # @retry(stop_max_attempt_number=3)
    def _parse_url(self, url):
        response = requests.get(url, headers=self.headers, timeout=5)
        return response.content.decode()

    def parse_url(self):  # 发送请求，获取响应
        while True:
            url = self.url_queue.get()
            print(url)
            try:
                html_str = self._parse_url(url)
            except:
                html_str = None
            # return html_str
            self.html_str_queue.put(html_str)
            self.url_queue.task_done()

    def get_content_list(self):  # 提取数据
        while True:
            html_str = self.html_str_queue.get()
            if html_str is not None:
                html = etree.HTML(html_str)
                div_list = html.xpath("//div[@id='content-left']/div")  # 分组
                content_list = []
                for div in div_list:
                    item = {}
                    # 用户头像
                    item["author_img"] = div.xpath("./div[@class='author clearfix']//img/@src")
                    item["author_img"] = "https:" + item["author_img"][0] if len(item["author_img"]) > 0 else None
                    # 用户名字
                    item["author_name"] = div.xpath("./div[@class='author clearfix']//img/@alt")
                    item["author_name"] = item["author_name"][0] if len(item["author_name"]) else None
                    # 用户性别
                    item["author_gender"] = div.xpath(".//div[contains(@class,'articleGender')]/@class")
                    item["author_gender"] = item["author_gender"][0].split(" ")[-1].replace("Icon", "") if len(
                        item["author_gender"]) > 0 else None

                    # 用户年龄
                    item["author_age"] = div.xpath(".//div[contains(@class,'articleGender')]/text()")
                    item["author_age"] = item["author_age"][0] if len(item["author_age"]) > 0 else None
                    # 段子
                    item["content"] = div.xpath(".//div[@class='content']/span/text()")
                    item["content"] = [i.strip() for i in item["content"]]
                    # 段子图片
                    item["img_list"] = div.xpath(".//div[@class='thumb']//img/@src")
                    item["img_list"] = ["http:" + i for i in item["img_list"]]

                    # 好笑的数量
                    item["stats_vote"] = div.xpath(".//span[@class='stats-vote']/i/text()")
                    item["stats_vote"] = item["stats_vote"][0] if len(item["stats_vote"]) > 0 else None

                    # 评论数
                    item["stats_comments"] = div.xpath(".//span[@class='stats-comments']//i/text()")
                    item["stats_comments"] = item["stats_comments"][0] if len(item["stats_comments"]) > 0 else None

                    # 神评论用户人
                    item["hot_comment_author_name"] = div.xpath(".//span[@class='cmt-name']/text()")
                    item["hot_comment_author_name"] = item["hot_comment_author_name"][0].rsplit("：", 1)[0] if len(
                        item["hot_comment_author_name"]) > 0 else None
                    # 神评论内容
                    item["hot_comment_content"] = div.xpath(".//div[@class='main-text']/text()")
                    item["hot_comment_content"] = item["hot_comment_content"][0] if len(
                        item["hot_comment_content"]) > 0 else None

                    # 神评论的点赞数
                    item["hot_comment_likenum"] = div.xpath(".//div[@class='likenum']/text()")
                    item["hot_comment_likenum"] = [i.strip() for i in item["hot_comment_likenum"] if len(i.strip()) > 0]
                    item["hot_comment_likenum"] = item["hot_comment_likenum"][0] if len(
                        item["hot_comment_likenum"]) > 0 else None
                    content_list.append(item)
                    print(item["hot_comment_author_name"], item["hot_comment_likenum"])
                # return content_list
                self.content_list_queue.put(content_list)
            else:
                self.content_list_queue.put([])
            self.html_str_queue.task_done()

    def save_content_list(self):
        while True:
            content_list = self.content_list_queue.get()
            with open("qiubai.csv", "a", encoding='utf-8') as f:
                for content in content_list:
                    temp_list = [content["author_name"], content["content"][0] if len(content["content"]) > 0 else None, content["stats_vote"], content["img_list"][0] if len(content["img_list"]) > 0 else None]
                    temp_str = ','.join([str(i) for i in temp_list])
                    # f.write(json.dumps(content, ensure_ascii=False))
                    f.write(temp_str+"\n")

            print("保存成功")
            self.content_list_queue.task_done()

    def run(self):  # 实现主要逻辑
        # 1.url list
        thread_list = []
        url_thread = threading.Thread(target=self.get_url_list)
        thread_list.append(url_thread)

        # 2.遍历，发送请求，获取响应
        for i in range(10):
            parse_thread = threading.Thread(target=self.parse_url)
            thread_list.append(parse_thread)

        # 3.提取数据
        get_cont_thread = threading.Thread(target=self.get_content_list)
        thread_list.append(get_cont_thread)

        # 4.保存
        save_cont_thread = threading.Thread(target=self.save_content_list)
        thread_list.append(save_cont_thread)

        for t in thread_list:
            t.setDaemon(True)  #设置为守护线程
            t.start()

        for q in [self.url_queue,self.html_str_queue,self.content_list_queue]:
            # 让主线程等待队列任务结束，全部的队列计数为0的时候，join失效
            q.join()

if __name__ == '__main__':
    qiubai = QiubaiSpider()
    qiubai.run()
