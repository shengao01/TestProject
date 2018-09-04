# -*- coding: utf-8 -*-
import scrapy
import re
import time
from urllib import parse
from scrapy.http import Request
from JobboleScrapy.items import JobbolescrapyItem


class JobboleSpider(scrapy.Spider):
    name = 'jobbole'
    allowed_domains = ['blog.jobbole.com']
    start_urls = ['http://blog.jobbole.com/all-posts/']

    def parse(self, response):
        post_nodes = response.css("#archive .floated-thumb .post-thumb")

        for post_node in post_nodes:
            # 获取文章url
            post_url = post_node.css("a::attr(href)").extract_first()
            # 获取封面图片url
            img_url = post_node.css("a img::attr(src)").extract_first()

            yield Request(url=parse.urljoin(response.url, post_url), meta={'front_img_url': img_url},
                          callback=self.parse_detail)
        # 获取下一页的url
        next_url = response.css("span.page-numbers.current+a::attr(href)").extract_first("")
        if next_url:
            yield Request(url=parse.urljoin(response.url, next_url), callback=self.parse)

    def parse_detail(self, response):
        article_item = JobbolescrapyItem()
        title = response.css(".entry-header h1::text").extract()[0]
        print(title)

        match_date = re.match("([0-9/]*)", response.css(".entry-meta-hide-on-mobile::text").extract()[0].strip())
        if match_date:
            public_date = match_date.group(1)

        content = response.css(".entry *::text").extract()
        # 对content进行特殊处理，并非所有的文章内容都在entry中
        if content is None:
            content = response.css("crayon-main *::text").extract()

        front_img_url = response.meta['front_img_url']

        tags_list_css = response.css(".entry-meta-hide-on-mobile a::text").extract()
        tags_list_css = [ele for ele in tags_list_css if not ele.strip().endswith('评论')]
        # 将标签列表转为String，并加入','作为分隔符，以下操作为Python3语法
        tags = ','.join(str(s) for s in tags_list_css)
        # 获取评论数，正则表达式匹配，仅保留数字
        ma_comments_css = re.match(".*?(\d+).*", response.css("a[href='#article-comment'] span::text").extract_first())
        if ma_comments_css:
            comment_nums = ma_comments_css.group(1)
        else:
            comment_nums = 0
        # print(comment_nums)

        article_item["title"] = title
        article_item["public_date"] = public_date
        article_item["article_url"] = response.url
        article_item["article_img_url"] = front_img_url
        article_item["tags"] = tags
        article_item["comment_nums"] = comment_nums
        article_item["content"] = ''.join(content)

        yield article_item
