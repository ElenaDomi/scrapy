#!/usr/bin/python
# -*- coding: UTF-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from ydd import items
import re

class Shuichan(CrawlSpider):
    name = "shuichan"
    allowed_domains = ["shuichan.cc"]
    start_urls = [
        "http://www.shuichan.cc/flea"
    ]

    rules = (
        Rule(LinkExtractor(allow=('flea_listtype.asp',))),
        Rule(LinkExtractor(allow=('flea_view-*', )), callback='parse_item'),
    )
    pattern = re.compile(r'\d+')

    def parse_item(self, response):
        # self.log('%s' % response.url)
        item = items.ShuichanItem()
        text_list = response.css('.tf  td ::text').extract()
        item_text = []
        if text_list is not None and isinstance(text_list, list):
            len_text_list = len(text_list)
            tmp_text = ''
            for i in range(1, len_text_list-1):
                text = clean(text_list[i])
                if len(text) > 0:
                    if '：' in text:
                        item_text.append(tmp_text)
                        tmp_text = text
                        if not tmp_text.endswith('：'):
                            item_text.append(tmp_text)
                            tmp_text = ''
                    else:
                        tmp_text += text
        for text in item_text:
            if len(text) > 0:
                if '：' in text:
                    key_value = text.split('：', 2)
                    key = get_key(key_value[0])
                    if (len(key_value) > 1):
                        value = key_value[1]
                    else:
                        value = ''
                    if key == 'views' and len(value) > 1:
                        value = value.replace('次', '')
                    elif key == 'publish' and len(value) > 0:
                        value = value[0:10] + ' '+ value[10:]
                    item[key] = value
        content_list = response.css('.htd::text').extract()
        if content_list is not None and isinstance(content_list, list):
            content = ''
            len_content_list = len(content_list)
            for i in range(1, len_content_list):
                content += content_list[i]
            item['content'] = content
        item['id'] = self.pattern.findall(response.url)[0]
        yield item

def clean(str):
    return str.encode('utf-8')\
        .replace(' ','')\
        .replace('（', '')\
        .replace('）', '')\
        .replace(' ','')\
        .replace('点击查看信息','')\
        .strip()

def get_key(key):
    if key == '发布人':
        return 'publisher'
    elif key == '手机':
        return 'mobile'
    elif key == '电话':
        return 'phone'
    elif key == '价格':
        return 'price'
    elif key == '电子邮件':
        return 'email'
    elif key == '所在地':
        return 'address'
    elif key == '联系人':
        return 'contacts'
    elif key == '网址':
        return 'website'
    elif key == '发布时间':
        return 'publish'
    elif key == '过期时间':
        return 'expired'
    elif key == '该信息已被浏览':
        return 'views'
    else:
        return 'unknown'