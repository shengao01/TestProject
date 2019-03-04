# -*- coding:utf-8 -*-
import requests
from lxml import etree
import pymysql
import time
import woff2otf
import re
from fontTools.ttLib import TTFont
import chardet

class MaoyanSpider():
    def __init__(self):

        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36",
            "Accept": "text / html, application / xhtml + xml, application / xml;q = 0.9, image / webp, * / *;q = 0.8",
            "Accept - Encoding": "gzip, deflate, sdch",
            "Accept - Language": "zh - CN, zh;q = 0.8",
            "Cache - Control": "max - age = 0",
            "Connection": "keep - alive",
            "Host": "maoyan.com",
            "Referer": "http: // maoyan.com / films"
            }
        # self.headers = {
        #     "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        #     "Accept-Encoding": "gzip, deflate, br",
        #     "Accept-Language": "zh-CN,zh;q=0.8",
        #     "Cache-Control": "max-age=0",
        #     "Connection": "keep-alive",
        #     "Upgrade-Insecure-Requests": "1",
        #     "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        #     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36",
        #     "Host": "maoyan.com"
        #
        # }

    def get_url_list(self):
        url_list = []
        for i in range(5):
            url_temp = "http://maoyan.com/films?offset={}".format(
                i * 30)
            url_list.append(url_temp)
        return url_list

    def parse_url(self, url):
        try:
            response = requests.get(url, headers=self.headers, timeout=500)
            print("休息2秒")
            time.sleep(2)
            if response.status_code == 200:
                print("ok")
                response.encoding = response.apparent_encoding
                return response

            else:
                print('无效请求')
                return None
        except:
            print("请求失败")

    def getHtml(self, html):
        link_list = []
        l = []
        if html:
            html = etree.HTML(html)

            print("开始解析")

            title_list = html.xpath("//dl[@class='movie-list']/dd//div[contains(@class, 'movie-item-title')]/a/text()")
            print(title_list)
            # 电影名称
            src_list = html.xpath("//dl[@class='movie-list']/dd//img[2]/@src")
            print(src_list)
            # 图片地址
            # num_list = html.xpath("//dl[@class='movie-list']/dd//div[contains(@class, 'channel-detail-orange')]//text()")
            num_list = [''.join(n.xpath(".//text()")) for n in
                        html.xpath("//dl[@class='movie-list']/dd//div[contains(@class, 'channel-detail-orange')]")]
            # 数字需要拼接
            print(num_list)
            a_list = html.xpath("//dl[@class='movie-list']/dd//a/@href")
            print(a_list)
            # 相对地址需要拼接
            try:
                # img_list = hml.xpath('//div[@class="neirong"]//@src')[0]
                for i in a_list:
                    if 'http' in i:
                        a_url = i
                    else:
                        a_url = 'http://maoyan.com' + i
                    print('地址>>>>>' + a_url)
                    link_list.append(a_url)
            except:
                print("地址拼接失败")
            # 请求详情页
            for x in link_list:
                res = requests.get(x, headers=self.headers)
                if res.status_code == 200:


                    res.encoding=res.apparent_encoding
                    res = res.content.decode()
                    # print(res)
                    htm = etree.HTML(res)
                    # print(htm)
                    en_name = htm.xpath("/html/body/div[3]/div/div[2]/div[1]/div/text()")#英文名字

                    genre = htm.xpath("/html/body/div[3]/div/div[2]/div[1]/ul/li[1]/text()")#类型

                    try:
                        sty = htm.xpath("/html/head/style/text()")
                        # cmp=re.compile(' //vfile.meituan.net/colorstone /（.* ?）.eot')

                        # cmp = re.compile(",\n           url\('(//.*.woff)'\) format\('woff'\)")
                        # print cmp
                        rst = re.findall("src: url\('(.*?)'\);", sty)
                        # print rst[0]
                        ttf = requests.get("http:" + rst[0], stream=True)
                        # print ttf
                        with open("maoyan.woff", "wb") as pdf:
                            for chunk in ttf.iter_content(chunk_size=1024):
                                if chunk:
                                    pdf.write(chunk)
                        # 转换woff字体为otf字体
                        woff2otf.convert('maoyan.woff', 'maoyan.otf')
                        # 解析字体库font文件
                        baseFont = TTFont('base.otf')
                        maoyanFont = TTFont('maoyan.otf')
                        uniList = maoyanFont['cmap'].tables[0].ttFont.getGlyphOrder()
                        numList = []
                        baseNumList = ['.', '3', '5', '1', '2', '7', '0', '6', '9', '8', '4']
                        baseUniCode = ['x', 'uniE64B', 'uniE183', 'uniED06', 'uniE1AC', 'uniEA2D', 'uniEBF8',
                                       'uniE831', 'uniF654', 'uniF25B', 'uniE3EB']
                        for i in range(1, 12):
                            maoyanGlyph = maoyanFont['glyf'][uniList[i]]
                            for j in range(11):
                                baseGlyph = baseFont['glyf'][baseUniCode[j]]
                                if maoyanGlyph == baseGlyph:
                                    numList.append(baseNumList[j])
                                    break
                        uniList[1] = 'uni0078'
                        utf8List = [eval("u'\u" + uni[3:] + "'").encode("utf-8") for uni in uniList[1:]]

                        # 获取发帖内容
                        movie_wish = htm.xpath("/html/body/div[3]/div/div[2]/div[3]/div[2]/div//text()")[0].text_content().replace(' ', '').replace('\n', '').encode('utf-8')
                        movie_name = htm.xpath("/html/body/div[3]/div/div[2]/div[1]/h3/text()")[0].text_content().replace(' ', '').replace('\n', '').encode('utf-8')

                        print( movie_name,movie_wish)

                        print('---------------after-----------------')
                        for i in range(len(utf8List)):
                            movie_wish = movie_wish.replace(utf8List[i],numList[i])
                        print(movie_name, movie_wish)
                    except:
                        print("规则匹配错误")
                    ftime = htm.xpath("/html/body/div[3]/div/div[2]/div[1]/ul/li[2]/text()")  # 产地和时长
                    # print("处理前",ftime)
                    from_time= re.sub(r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+|\\n", "", str(ftime))
                    print("处理后",from_time)
                    time_where = htm.xpath("/html/body/div[3]/div/div[2]/div[1]/ul/li[3]/text()")# 上映时间和地区
                    print(en_name, genre, from_time, time_where)

                    mem= htm.xpath("//*[@id='app']/div/div[1]/div/div[2]/div[1]/div[2]/div[2]/div//text()")
                    # print("处理前",mem)
                    # string = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', ", '', str(mem))
                    # print("处理中",string)
                    member= re.sub(r"[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+|\\n", "", str(mem))
                    print("处理后",member)
                    intrd = htm.xpath("//*[@id='app']/div/div[1]/div/div[2]/div[1]/div[1]//text()")
                        # string = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', ", '', str(intr))

                        # intrd = re.sub(r'\\xa0|\\r\\n', '', intr)
                    comm_al = htm.xpath(
                            "//*[@id='app']/div/div[1]/div/div[2]/div[1]/div[4]//span[@class='name']//text()")[0]
                        # string = re.sub("[\s+\.\!\/_,$%^*(+\"\')]+|[+——()?【】“”！，。？、~@#￥%……&*（）]+', ", '', str(m))
                        #
                        # mean = re.sub(r'\\xa0|\\r\\n', '', string)
                    comm_tl = htm.xpath(
                            "//*[@id='app']/div/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/ul/li//div[@class='time']/@title")[0]
                    comm_dl = htm.xpath(
                            "//*[@id='app']/div/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/ul/li//div[@class='comment-content']/text()")[0]
                    comm_zl = htm.xpath(
                            "//*[@id='app']/div/div[1]/div/div[2]/div[1]/div[4]/div[2]/div/ul/li//span[@class='num']/text()")[0]
                    print(member, intrd, comm_al, comm_dl, comm_tl, comm_zl)


                # else:
                #     print("详情页请求失败")
            # replay_list = html.xpath("")
            # name_list = html.xpath("")
            for i in range(len(title_list) - 1):
                # 通过列表长度取下标
                title = title_list[i]
                src = src_list[i]
                # = re_list[i]
                num = num_list[i]
                link = link_list[i]
                print(title, src, num, link)
                # 插入数据库
                # l.append([title, src, num, link])
                # conn = pymysql.connect(host='127.0.0.1', user='root', password='root', db='box_office', charset="utf8")
                #
                # cur = conn.cursor()
                # print("插入中")
                #
                # sql = 'INSERT INTO maoyan(title,src,num,link) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)'
                # print(l)
                #
                # #       row_per + str(6), sum_day + str(7), cur_day + str(8))
                # cur.executemany(sql, l)
                # conn.commit()
                #
                # cur.close()
                # print("插入成功")
                # conn.close()

    def run(self):
        url_list = self.get_url_list()
        for i in url_list:
            response = self.parse_url(i)
            html = response.text
            r = self.getHtml(html)


if __name__ == '__main__':
    # if __name__ == '__main__':
    spider = MaoyanSpider()
    print("检索中")
    spider.run()

#
