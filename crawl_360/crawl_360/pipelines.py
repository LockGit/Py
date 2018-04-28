# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from crawl_360.items import ButianItem
from crawl_360.models.db import DBSession
from crawl_360.models.models import Butian


class Crawl360Pipeline(object):
    def __init__(self):
        self.db_session = DBSession()

    def process_item(self, item, spider):
        if isinstance(item, ButianItem):
            data_item = Butian(**item)
            # 数据入库
            self.db_session.add(data_item)
            try:
                self.db_session.commit()
            except Exception, e:
                print e.message
                self.db_session.rollback()
        return item

    def close_spider(self, spider):
        self.db_session.close()
