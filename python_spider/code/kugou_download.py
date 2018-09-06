# coding:utf-8
import requests
import json
import copy
import hashlib


class KuGouSpider(object):
    def __init__(self):
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Connection': 'keep-alive',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36',
        }
        self.search_url = 'http://songsearch.kugou.com/song_search_v2?page=1&filter=0&bitrate=0&isfuzzy=0&tag=em&inputtype=2&platform=PcFilter&userid=482381247&clientver=8202&iscorrection=7&area_code=1'

    def music_search(self):
        keyword = str(input('输入关键字:'))
        search_url = self.search_url + '&keyword=%s' % keyword
        total = json.loads(requests.get(search_url, headers=self.headers).text)['data']['total']
        search_url = search_url + 'page=1&pagesize=%d' % total
        music_list = json.loads(requests.get(search_url, headers=self.headers).text)['data']['lists']
        item, items, index = {}, [], 0
        for music in music_list:
            if music['SQFileHash'] != '' and music['SQFileHash'] != '00000000000000000000000000000000':
                hash = str.lower(music['SQFileHash'])
                key = hashlib.md5((hash + 'kgcloudv2').encode('utf-8')).hexdigest()
                url = 'http://trackercdnbj.kugou.com/i/v2/?cmd=23&hash={}&key={}&pid=1&behavior=download'.format(hash,
                                                                                                                 key)
                ret = json.loads(requests.get(url, headers=self.headers).text)
                if 'url' in ret.keys():
                    index += 1
                    item['index'] = index
                    item['SongName'] = music['SongName']
                    item['Singer'] = music['SingerName']
                    item['url'] = ret['url']
                    items.append(copy.deepcopy(item))
        return items

    def download(self, item):
        ExtName = item['url'].split('.')[-1]
        FilePath = './%s.%s' % (item['SongName'], ExtName)
        with open(FilePath, 'wb') as f:
            print('正在下载   %s.........' % (item['SongName']))
            f.write(requests.get(item['url']).content)

    def run(self):
        items = self.music_search()
        print('---------------------查询到%d首无损音乐---------------------' % len(items))
        for item in items:
            print('序号:%s   歌名:%s   歌手:%s   链接:%s' % (item['index'], item['SongName'], item['Singer'], item['url'],))
        Action = input('是否需要下载(Y/N):')
        if Action == 'Y' or 'y':
            Action2 = input('输入序号(支持多首下载,用逗号隔开,全部下载直接回车):')
            if len(Action2) > 0:
                for index in Action2.split(','):
                    if int(index) <= len(items):
                        item = items[int(index) - 1]
                        self.download(item)
            else:
                for item in items:
                    self.download(item)
        else:
            pass


if __name__ == '__main__':
    start = KuGouSpider()
    start.run()
