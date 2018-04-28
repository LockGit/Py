# -*- coding: utf-8 -*-
import scrapy

from crawl_360.items import ButianItem
import time


class ButianSpider(scrapy.Spider):
    name = 'butian'
    allowed_domains = ['butian.360.cn/Loo', 'butian.360.cn']
    start_urls = ['http://butian.360.cn/Loo/']

    def parse(self, response):
        self.logger.info('strart parse dst page ...')
        item = ButianItem()
        # import ipdb
        # ipdb.set_trace()
        for sel in response.xpath('//ul[@class="loopListBottom"]/li'):
            item['author'] = sel.xpath('dl/dd/span[1]/text()').extract_first(default='').strip()
            item['company_name'] = sel.xpath('dl/dd/a/text()').extract_first(default='').strip()
            item['vul_name'] = sel.xpath('dl/dd/span[3]/text()').extract_first(default='').replace(u'的一个', '').strip()
            item['vul_level'] = sel.xpath('dl/dd[2]/strong[@class="loopHigh"]/text()').extract_first(default='').strip()
            item['vul_money'] = sel.xpath('dl/p[@class="loopJiangjin"]/text()').extract_first(default=0)
            item['vul_find_time'] = sel.xpath('dl/dd[2]/em/text()').extract_first(default='').strip()
            item['link_url'] = response.url.strip()
            item['create_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
            self.logger.info('find item data is:%s' % (item,))
            yield item

        next_page = response.xpath(u'//div[@class="btPage page"]/a[contains(text(),"下一页")]/@href').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            self.logger.info('next page url is:%s' % (next_page,))
            yield scrapy.Request(url=next_page, callback=self.parse)
