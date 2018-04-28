# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Crawl360Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ButianItem(scrapy.Item):
    author = scrapy.Field()  # 作者
    company_name = scrapy.Field()  # 企业名称
    vul_name = scrapy.Field()  # SQL注入漏洞
    vul_level = scrapy.Field()  # 高危
    vul_type = scrapy.Field()  # 通用型
    vul_money = scrapy.Field()  # 奖励
    vul_find_time = scrapy.Field()  # 时间
    link_url = scrapy.Field()  # 抓取url
    create_time = scrapy.Field()  # 创建时间
