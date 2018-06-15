# -*- coding: utf-8 -*-
import datetime

import re
from urllib.parse import urljoin

import scrapy

from RentSeeking.items import AmpDetailInfoItem, ApmBaseInfoItem


class TongchengSpider(scrapy.Spider):
    name = 'tongcheng'
    allowed_domains = ['sz.58.com']
    start_urls = ['http://sz.58.com/chuzu/sub/?pagetype=ditie']
    headers = {}
    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': .5,
        'AUTOTHROTTLE_MAX_DELAY': 1.5,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'AUTOTHROTTLE_DEBUG': False
    }

    def parse(self, response):
        target_urls = response.xpath('//*[@class="secitem secitem_fist subway"]/dd/a/@href').extract()
        subways = response.xpath('//*[@class="secitem secitem_fist subway"]/dd/a/text()').extract()
        subways = [x.strip() for x in subways]
        for url, subway in zip(target_urls, subways):
            if '号线' in subway:
                yield scrapy.Request(url=urljoin(self.start_urls[-1], url), meta={'subway': subway},
                                     callback=self.parse_base_info, headers=self.headers)

    def parse_base_info(self, response):
        subway = response.meta.get('subway')
        # 判断有没有下一页

        next_page_url = response.xpath('//*[@id="bottom_ad_li"]/div[2]/a[4]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse_base_info, meta={'subway': subway},
                                 headers=self.headers)

        # 获取数据
        data_list = response.xpath('//*[@class="listUl"]/li')
        for data in data_list:
            item = ApmBaseInfoItem()
            item['apm_name'] = data.xpath('./div[2]/h2/a/text()').extract_first()
            apm_url = data.xpath('./div[2]/h2/a/@href').extract_first()
            item['apm_url'] = apm_url
            item['cell_name'] = data.xpath('./div[2]/p[2]/a[2]/text()').extract_first()
            item['cell_type'] = data.xpath('./div[2]/p[1]/text()').extract_first()
            if item['cell_type']:
                item['area'] = item['cell_type'].split(' ')[-1]
                item['area'] = re.search('\d+', item['area']).group()
                item['cell_type'] = item['cell_type'].split(' ')[0]
            else:
                item['area'] = '不详'
            item['built_year'] = '不详'
            item['price'] = data.xpath('./div[3]/div[2]/b/text()').extract_first()
            item['subway'] = subway
            item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 解析租房具体信息
            meta = {
                'apm_name': item['apm_name'],
                'price': item['price'],
                'cell_type': item['cell_type'],
                'area': item['area'],
            }
            if apm_url:
                yield scrapy.Request(url=apm_url, meta=meta, callback=self.parse_detail_info,
                                 headers=self.headers, dont_filter=True)
            # 返回数据
            yield item

    def parse_detail_info(self, response):
        apm_name = response.meta.get('apm_name')
        price = response.meta.get('price')
        cell_type = response.meta.get('cell_type')
        area = response.meta.get('area')
        item = AmpDetailInfoItem()
        item['apm_name'] = apm_name
        item['price'] = price
        item['area'] = area
        item['apm_detail_url'] = response.url
        item['floor'] = response.xpath('//*[@class="f14"]/li[3]/span[2]/text()').extract_first()
        if item['floor']:
            item['orientation'] = item['floor'].split('  ')
            if len(item['orientation']) > 2:
                item['orientation'] = item['orientation'][1]
            else:
                item['orientation'] = '不详'
        else:
            item['orientation'] = '不详'
        if item['floor']:
            item['floor'] = item['floor'].split('  ')[0]
        item['traffication'] = response.xpath('//*[@class="f14"]/li[5]/em/text()').extract_first()
        item['location'] = ','.join( response.xpath('//*[@class="f14"]/li[5]/span[2]/a/text()').extract())
        item['cell_type'] = cell_type

        item['contact'] = response.xpath('//*[@id="bigCustomer"]/p[1]/a/text()').extract_first()
        if item['contact']:
            item['contact_identity'] = re.search('\(.*?\)', item['contact'])
            if item['contact_identity']:
                item['contact_identity'] = item['contact_identity'].group()
            else:
                item['contact_identity'] = '不详'
        else:
            item['contact_identity'] = '不详'
        item['phone'] = response.xpath('//*[@class="house-chat-phone"]/span/text()').extract_first()
        item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield item
