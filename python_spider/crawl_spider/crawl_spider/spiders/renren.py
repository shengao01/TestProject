# -*- coding: utf-8 -*-
import scrapy
import re

class RenrenSpider(scrapy.Spider):
    name = 'renren'
    allowed_domains = ['renren.com']
    start_urls = ['http://www.renren.com/481421029/profile']

    def start_requests(self):
        headers = {
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36',
            # 'cookie':'anonymid=jauzg80u-sny209; _r01_=1; wp=0; depovince=GW; jebecookies=a73a9f88-9b18-4436-94b2-01c896327fb9|||||; JSESSIONID=abcVAwYcqdD0X_0iu5Obw; ick_login=d27f7a39-1ace-4621-9872-9acd32dad9ab; _de=A4A24BE4950F681622D1361953B7C8FA; p=b1b3328b7421638422f6e9b053cf31d19; first_login_flag=1; ln_uact=13156505806; ln_hurl=http://hdn.xnimg.cn/photos/hdn421/20130514/1020/h_main_cPLt_c0b2000009f0113e.jpg; t=490c3312cd001284c9d1a38089f5554e9; societyguester=490c3312cd001284c9d1a38089f5554e9; id=481421029; xnsid=971aa31e; loginfrom=syshome; ch_id=10016; wp_fold=0'
        }
        # cookie = 'anonymid=jauzg80u-sny209; _r01_=1; wp=0; depovince=GW; jebecookies=a73a9f88-9b18-4436-94b2-01c896327fb9|||||; JSESSIONID=abcVAwYcqdD0X_0iu5Obw; ick_login=d27f7a39-1ace-4621-9872-9acd32dad9ab; _de=A4A24BE4950F681622D1361953B7C8FA; p=b1b3328b7421638422f6e9b053cf31d19; first_login_flag=1; ln_uact=13156505806; ln_hurl=http://hdn.xnimg.cn/photos/hdn421/20130514/1020/h_main_cPLt_c0b2000009f0113e.jpg; t=490c3312cd001284c9d1a38089f5554e9; societyguester=490c3312cd001284c9d1a38089f5554e9; id=481421029; xnsid=971aa31e; loginfrom=syshome; ch_id=10016; wp_fold=0'
        cookie = 'anonymid=jauzg80u-sny209; _r01_=1; wp=0; depovince=GW; jebecookies=a73a9f88-9b18-4436-94b2-01c896327fb9|||||; ick_login=d27f7a39-1ace-4621-9872-9acd32dad9ab; _de=A4A24BE4950F681622D1361953B7C8FA; p=b1b3328b7421638422f6e9b053cf31d19; first_login_flag=1; ln_uact=13156505806; ln_hurl=http://hdn.xnimg.cn/photos/hdn421/20130514/1020/h_main_cPLt_c0b2000009f0113e.jpg; t=490c3312cd001284c9d1a38089f5554e9; societyguester=490c3312cd001284c9d1a38089f5554e9; id=481421029; xnsid=971aa31e; loginfrom=syshome; ch_id=10016; JSESSIONID=abctygiXECzlT7S4l9Obw; wp_fold=0'
        cookie_dict = {i.split('=')[0]:i.split('=')[1] for i in cookie.split('; ')}
        yield scrapy.Request(
            self.start_urls[0],
            callback=self.parse,
            headers=headers,
            cookies=cookie_dict
        )

    def parse(self, response):
        with open('renren.html','wb') as f:
            f.write(response.body)
        yield scrapy.Request(
            'http://friend.renren.com/managefriends',
            callback=self.parse_detail,
        )

    def parse_detail(self,response):
        with open('renren1.html','wb') as f:
            f.write(response.body)
        li = re.findall(r'张',response.body.decode())
        print(li)
