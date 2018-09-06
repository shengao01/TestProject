import requests
import json


class TV_spider():
    # 初始化链接和相关代理
    def __init__(self):

        # movie_list
        self.url_temp = "https://movie.douban.com/j/search_subjects?type=movie&tag=%E7%BB%8F%E5%85%B8&sort=rank&page_limit=20&page_start={}"
        # tv_list
        # self.url_temp = "https://movie.douban.com/j/search_subjects?type=tv&tag=%E7%BE%8E%E5%89%A7&sort=recommend&page_limit=20&page_start={}"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        }

    def url_handle(self):
        url_list = [self.url_temp.format(i * 20) for i in range(0, 10)]
        return url_list

    def parse_url(self, url):
        resp = requests.get(url, headers=self.headers)
        dict = json.loads(resp.text)
        # print(dict)
        return dict

    def run(self):
        url_list = self.url_handle()
        # print(url_list)
        movie_list = []
        name_list = []
        url_set = []
        for url in url_list:
            resp_dict = self.parse_url(url)
            movie_list.extend(resp_dict['subjects'])
        print(movie_list)
        # list_data = str(movie_list).encode()
        # with open('movie_list.txt','wb') as f:
        #     f.write(list_data)

        # for part in movie_list:
        #     name_list.append(part['title'])
        #
        # for part in movie_list:
        #     url_set.append(part['cover'])
        #
        for part in movie_list:
            url = part['cover']
            resp_img = requests.get(url, headers=self.headers)
            # img_data = resp_img.content
            file_path = './mv_pic/'+part['rate']+part['title']+'.jpg'
            print(file_path)
            with open(file_path,'wb') as f:
                f.write(resp_img.content)


if __name__ == '__main__':
    tv = TV_spider()
    tv.run()
