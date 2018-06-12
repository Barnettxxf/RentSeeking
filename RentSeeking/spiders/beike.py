# -*- coding: utf-8 -*-
import datetime

import re
from urllib.parse import urljoin

import scrapy

from RentSeeking.items import AmpDetailInfoItem, ApmBaseInfoItem


class BeikeSpider(scrapy.Spider):
    name = 'beike'
    allowed_domains = ['sz.zu.ke.com']
    start_urls = ['https://sz.zu.ke.com/ditiezufang/']
    headers = {

    }

    def parse(self, response):
        target_urls = response.xpath('//*[@id="filter"]/ul[3]/li/a/@href').extract()
        subways = response.xpath('//*[@id="filter"]/ul[3]/li/a/text()').extract()
        for url, subway in zip(target_urls, subways):
            if '号线' in subway:
                yield scrapy.Request(url=urljoin(self.start_urls[-1], url), meta={'subway': subway},
                                     callback=self.parse_base_info, headers=self.headers)

    def parse_base_info(self, response):
        subway = response.meta.get('subway')

        # 判断有没有下一页
        total_page = response.xpath('//*[@id="content"]/div[1]/div[2]/@data-totalpage').extract_first()
        if not total_page:
            return
        current_page = response.xpath('//*[@id="content"]/div[1]/div[2]/@data-curpage').extract_first()
        if 'pg%s' % current_page not in response.url:
            url = urljoin(response.url, 'pg%s' % current_page)
        else:
            url = None
        if url is None:
            url = response.url.replace('pg%s' % current_page, 'pg%d' % (int(current_page) + 1))
        else:
            url = url.replace('pg%s' % current_page, 'pg%d' % (int(current_page) + 1))
        if int(current_page) <= int(total_page):
            yield scrapy.Request(url=url, callback=self.parse_base_info, meta={'subway': subway}, headers=self.headers)

        # 获取数据
        data_list = response.xpath('//*[@id="content"]/div[1]/div[1]')
        for data in data_list:
            item = ApmBaseInfoItem()
            item['apm_name'] = data.xpath('./div[1]/div/p[1]/a/text()').extract_first()
            item['apm_url'] = data.xpath('./div[1]/div/p[1]/a/@href').extract_first()
            item['apm_url'] = urljoin(self.start_urls[-1], item['apm_url'])
            item['cell_name'] = data.xpath('./div[1]/div/p[3]/text()').extract_first()
            item['cell_type'] = data.xpath('./div[1]/div/p[2]/text()[2]').extract_first()
            item['area'] = data.xpath('./div[1]/div/p[2]/text()[1]').extract_first()
            item['built_year'] = '不详'
            item['price'] = data.xpath('./div[1]/div/span/em/text()').extract_first()
            item['subway'] = subway
            item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 解析租房具体信息
            meta = {
                'apm_name': item['apm_name'],
                'price': item['price'],
                'cell_type': item['cell_type'],
                'area': item['area'],
                'subway': item['subway'],
            }
            yield scrapy.Request(url=item['apm_url'],
                                 meta=meta, callback=self.parse_detail_info, headers=self.headers)
            # 返回数据
            yield item

    def parse_detail_info(self, response):
        apm_name = response.meta.get('apm_name')
        price = response.meta.get('price')
        cell_type = response.meta.get('cell_type')
        area = response.meta.get('area')
        subway = response.meta.get('subway')
        item = AmpDetailInfoItem()
        item['apm_name'] = apm_name
        item['price'] = price
        item['area'] = area
        item['apm_detail_url'] = response.url
        item['floor'] = '不详'
        item['traffication'] = subway
        item['location'] = response.xpath('//*[@id="info"]/div/p[2]/text()').extract_first()
        if not item['location']:
            item['location'] = ','.join(
                [x.replace('距离', '').strip() for x in response.xpath('//*[@id="around"]/ul/li/text()').extract()])
        item['cell_type'] = cell_type
        item['orientation'] = '不详'
        item['contact'] = response.xpath('//*[@id="aside"]/div/ul/li/p[1]/span/text()').extract_first()
        if not item['contact']:
            item['contact'] = response.xpath('//*[@id="aside"]/ul/li/p[1]/span[1]/text()').extract_first()
        item['contact_identity'] = response.xpath('//*[@id="aside"]/div/ul/li/p[2]/text()').extract_first()
        if not item['contact_identity']:
            item['contact_identity'] = response.xpath('//*[@id="aside"]/ul/li/p[2]/text()').extract_first()
        item['phone'] = response.xpath('//*[@id="aside"]/div/ul/li/p[3]/text()').extract_first()
        if not item['phone']:
            item['phone'] = response.xpath('//*[@id="aside"]/ul/li/p[3]/text()').extract_first()
        item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield item
