# -*- coding: utf-8 -*-
import datetime
from urllib.parse import urljoin

import re
import scrapy

from RentSeeking.items import AmpDetailInfoItem, ApmBaseInfoItem


class ZiruSpider(scrapy.Spider):
    name = 'ziru'
    allowed_domains = ['sz.ziroom.com']
    start_urls = ['http://sz.ziroom.com/z/nl/z3.html']
    headers = {

    }

    def parse(self, response):
        target_urls = response.xpath('//*[@id="selection"]/div/div/dl[3]/dd/ul/li/span/a/@href').extract()
        subways = response.xpath('//*[@id="selection"]/div/div/dl[3]/dd/ul/li/span/a/text()').extract()
        for url, subway in zip(target_urls, subways):
            if '号线' in subway:
                yield scrapy.Request(url=urljoin(self.start_urls[-1], url), meta={'subway': subway},
                                     callback=self.parse_base_info, headers=self.headers)

    def parse_base_info(self, response):
        subway = response.meta.get('subway')
        # 判断有没有下一页

        next_page_url = response.xpath('//*[@id="page"]/a[5]/@href').extract_first()
        if next_page_url:
            next_page_url = urljoin(self.start_urls[-1], next_page_url)
            yield scrapy.Request(url=next_page_url, callback=self.parse_base_info, meta={'subway': subway},
                                 headers=self.headers)

        # 获取数据
        data_list = response.xpath('//*[@id="houseList"]/li')
        for data in data_list:
            item = ApmBaseInfoItem()
            item['apm_name'] = data.xpath('./div[2]/h3/a/text()').extract_first()
            item['apm_url'] = data.xpath('./div[2]/h3/a/@href').extract_first()
            item['apm_url'] = urljoin(self.start_urls[-1], item['apm_url'])
            item['cell_name'] = data.xpath('./div[1]/a/img/@alt').extract_first()
            item['cell_type'] = '不详'
            item['area'] = data.xpath('./div[2]/div/p[1]/span[1]/text()').extract_first()
            if item['area']:
                item['area'] = re.search('\d+', item['area']).group()
            item['built_year'] = '不详'
            item['subway'] = subway
            item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

            location = data.xpath('./div[2]/h4/a/text()').extract_first()
            # 解析租房具体信息
            meta = {
                'apm_name': item['apm_name'],
                'area': item['area'],
                'location': location,
                'item': item
            }
            yield scrapy.Request(url=item['apm_url'], meta=meta, callback=self.parse_detail_info, headers=self.headers)

    def parse_detail_info(self, response):
        apm_name = response.meta.get('apm_name')
        base_info_item = response.meta.get('item')
        area = response.meta.get('area')
        location = response.meta.get('location')
        item = AmpDetailInfoItem()
        item['apm_name'] = apm_name
        item['price'] = response.xpath('//*[@id="room_price"]/text()').extract_first()
        if item['price']:
            item['price'] = item['price'][1:]
        base_info_item['price'] = item['price']
        item['area'] = area
        item['apm_detail_url'] = response.url
        item['floor'] = response.xpath('/html/body/div[3]/div[2]/ul/li[4]/text()').extract_first()
        if item['floor']:
            item['floor'] = item['floor'].strip().split('：')[1]
        item['traffication'] = ','.join([x.strip() for x in response.xpath('//*[@id="lineList"]/span/p/text()').extract()])
        item['location'] = location
        item['cell_type'] = response.xpath('/html/body/div[3]/div[2]/ul/li[3]/text()').extract_first()
        if item['cell_type']:
            item['cell_type'] = item['cell_type'].strip().split('：')[1]
        item['orientation'] = response.xpath('/html/body/div[3]/div[2]/ul/li[2]/text()').extract_first()
        if item['orientation']:
            item['orientation'] = item['orientation'].strip().split('：')[1]
        item['contact'] = '自如'
        item['contact_identity'] = '自如'
        item['phone'] = '请上网查...'
        item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield item
        yield base_info_item
