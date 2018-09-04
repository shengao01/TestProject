# coding:utf-8
# http://www.ximalaya.com/tracks/14420295.json
# {"id":14420295,"play_path_64":"http://audio.xmcdn.com/group13/M07/45/DF/wKgDXlcPliWjnPF3AFnYuTP9Lc8247.m4a","play_path_32":"http://audio.xmcdn.com/group8/M09/45/81/wKgDYFcPmEHSEKSbACJM1gBsvCc419.m4a","play_path":"http://audio.xmcdn.com/group13/M07/45/DF/wKgDXlcPliWjnPF3AFnYuTP9Lc8247.m4a","duration":727,"title":"\u6ed5\u738b\u9601\u5e8f","nickname":"365\u8bfb\u4e66","uid":33785482,"waveform":"group10/M06/43/F8/wKgDaVcPljezIG12AAAKaj33wjE1445.js","upload_id":"u_13341058","cover_url":"http://fdfs.xmcdn.com/group16/M05/45/A9/wKgDalcPln_j-e3ZAAIs25V9Sa4370.jpg","cover_url_142":"http://fdfs.xmcdn.com/group16/M05/45/A9/wKgDalcPln_j-e3ZAAIs25V9Sa4370_web_large.jpg","formatted_created_at":"4\u670814\u65e5 21:09","is_favorited":null,"play_count":102097,"comments_count":95,"shares_count":10,"favorites_count":255,"album_id":3048185,"album_title":"365\u8bfb\u4e66","intro":"\u4e3b\u64ad\uff1a\u6f6e\u7fbd\uff0c365\u5929\u6bcf\u5929\u66f4\u65b0\u4e00\u671f\u3002\u5fae\u4fe1\u516c\u4f17\u53f7\uff1a\u300c365\u8bfb\u4e66\u300d\uff08dus365) \u5fae\u535a\uff1a365\u8bfb\u4e66v\u3002 \u6587\u5b57\u7248\u5df2\u5728\u5fae\u4fe1\u516c\u4f17\u53f7\u3010365\u8bfb\u4e66\u3011\u53d1\u5e03 \u3002\u80cc\u666f\u97f3\u4e50\uff1a\u7fa4\u661f-\u59d1\u82cf\u884c\uff08\u7b1b\uff09\u2014\u2014\u7fa4\u661f-\u9e67\u9e2a\u98de\uff08\u7af9\u7b1b\uff09","have_more_intro":false,"time_until_now":"1\u5e74\u524d","category_name":"renwen","category_title":"\u4eba\u6587","played_secs":null,"is_paid":false,"is_free":null,"price":null,"discounted_price":null}

import requests
import json
import gevent
import re
from gevent import monkey


monkey.patch_all()
class Radio_spider():
    # 初始化链接和相关代理
    def __init__(self):
        # http://www.ximalaya.com/96373069/album/11709082/

        # http://www.ximalaya.com/tracks/60084104.json
        self.url_temp = "http://www.ximalaya.com/91044493/album/10188465/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36"
        }

    def parse_url(self):
        url = self.url_temp
        resp = requests.get(url, headers=self.headers)
        # dict = json.loads(resp.text)
        dict = resp.text
        pattern = re.compile(r'href="/\d+/sound/(\d+)/" hashlink title="(.*?)">')
        # href="/\d+/sound/(\d+)/" hashlink title="(.*?)">
        id_list = pattern.findall(dict)
        # print(dict)
        return id_list

    def get_url(self,url):
        resp = requests.get(url, headers=self.headers, timeout=10)
        dict = json.loads(resp.text)
        return dict

    def get_content(self, url, name):
        radio = requests.get(url, headers=self.headers, timeout=10)
        file_path = name[4:-2] + '.m4a'
        with open(file_path, 'wb') as f:
            f.write(radio.content)

    def run(self):
        id_list = self.parse_url()
        print(id_list)
        url_list = []
        for id in id_list:
            url = "http://www.ximalaya.com/tracks/"+str(id[0])+".json"
            url_list.append((url, id[1]))

        for url in url_list:
            url = url[0]
            dict = self.get_url(url)
            rad_url = dict['play_path_64']
            # name = str(dict['id'])
            name = url[1]
            print(rad_url)
            self.get_content(rad_url,name)
            # gevent.spawn(self.get_content,rad_url,name)


if __name__ == '__main__':
    radio = Radio_spider()
    radio.run()

