import requests
import re
# from lxml import etree
from queue import Queue
import threading


class WangyiSpider():
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        }
        self.part_url = "http://music.163.com"
        self.url_temp = "http://music.163.com/discover/playlist/?cat=%E9%92%A2%E7%90%B4&order=hot&limit=35&offset={}"
        self.url_queue = Queue()
        self.html_str_queue = Queue()
        self.content_list_queue = Queue()
        self.song_list_queue = Queue()
        self.url_queue1 = Queue()
        self.html_str_queue1 = Queue()

        with open("list.csv", "a", encoding="utf-8") as f:
            f.write("Title" + "\n")

    def get_url_list(self):
        # url_list = [self.url_temp.format(i * 35) for i in range(0, 38)]
        # return url_list
        for i in range(3):
            self.url_queue.put(self.url_temp.format(i * 35))

    def _parse_url(self, url):
        # 发送请求,获取响应
        resp = requests.get(url, headers=self.headers, timeout=5)
        return resp.content.decode()

    # 解析url获取页面内容的字符串
    def parse_url(self):
        while True:
            url = self.url_queue.get()
            try:
                html_str = self._parse_url(url)
            except:
                html_str = None
            # return html_str
            self.html_str_queue.put(html_str)
            self.url_queue.task_done()

    # 解析url获取页面内容的字符串
    def parse_url1(self):
        while True:
            url = self.url_queue1.get()
            try:
                html_str = self._parse_url(url)
            except:
                html_str = None
            # return html_str
            self.html_str_queue1.put(html_str)
            self.url_queue1.task_done()

    def get_content_list(self):
        while True:
            html_str = self.html_str_queue.get()
            if html_str is not None:
                # <a title="十一月 | 电音鉴赏指南⚡️Top100" href="/playlist?id=1995337890" class="msk"></a>
                pattern = re.compile(r'<a title="(.*?)" href="(.*?)" class="msk"></a>')
                div_list = pattern.findall(str(html_str))
                print(str(div_list))
                content_list = []
                for div in div_list:
                    item = {}
                    item["title"] = div[0]
                    item["href"] = self.part_url + div[1]
                    content_list.append(item)
                self.content_list_queue.put(content_list)
                print(str(content_list))
                    # self.content_list_queue.put(item)
            else:
                self.content_list_queue.put([])
            self.html_str_queue.task_done()

    # 通过歌单地址读取页面,并提取歌曲信息
    def get_song_list(self):
        while True:
            content_list = self.content_list_queue.get()
            for i in content_list:
                url = i["href"]
                self.url_queue1.put(url)
                # html = self.parse_url(url)
                html = self.html_str_queue1.get()
                pattern = re.compile(r'<li><a href="/song\?id=\d+">(.*?)</a>')
                song_list = pattern.findall(str(html))
                print(str(song_list))
                self.song_list_queue.put(song_list)
                self.html_str_queue1.task_done()
            self.content_list_queue.task_done()

    # 保存歌单信息到表格中
    def save_song_list(self):
        while True:
            list = self.song_list_queue.get()
            content_list = self.content_list_queue.get()
            for i in content_list:
                a = i["title"]
                with open("list.csv", "a", encoding="utf-8") as f:
                    temp_str = ",".join([str(i) for i in list])
                    f.write(a + temp_str + "\n")
            self.song_list_queue.task_done()
            self.content_list_queue.task_done()

    def run(self):
        # url_list = self.get_url_list()
        # for url in url_list:
        #     html_str = self.parse_url(url)
        #     content_list = self.get_content_list(html_str)
        thread_list = []
        url_thread = threading.Thread(target=self.get_url_list)
        thread_list.append(url_thread)

        # 2.遍历，发送请求，获取响应
        for i in range(5):
            parse_thread = threading.Thread(target=self.parse_url)
            thread_list.append(parse_thread)

        for i in range(5):
            parse1_thread = threading.Thread(target=self.parse_url1)
            thread_list.append(parse1_thread)

        # 3.提取数据
        get_cont_thread = threading.Thread(target=self.get_content_list)
        thread_list.append(get_cont_thread)

        # 4.读取歌曲列表信息
        get_song_thread = threading.Thread(target=self.get_song_list)
        thread_list.append(get_song_thread)

        # 5.保存歌曲列表信息
        for i in range(5):
            save_song_thread = threading.Thread(target=self.save_song_list)
            thread_list.append(save_song_thread)

        for t in thread_list:
            t.setDaemon(True)
            t.start()

        for q in [self.url_queue, self.url_queue1, self.html_str_queue, self.html_str_queue1, self.content_list_queue,self.song_list_queue]:
            # 让主线程等待队列任务结束，全部的队列计数为0的时候，join失效
            q.join()


if __name__ == '__main__':
    wy = WangyiSpider()
    wy.run()
