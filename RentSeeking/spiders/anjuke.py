# -*- coding: utf-8 -*-
from urllib.parse import urljoin

import re

import datetime
import scrapy

from RentSeeking.items import AmpDetailInfoItem, ApmBaseInfoItem


class AnjukeSpider(scrapy.Spider):
    name = 'anjuke'
    allowed_domains = ['sz.zu.anjuke.com']
    start_urls = ['https://sz.zu.anjuke.com/ditie/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.19 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Upgrade-Insecure-Requests': '1',
    }

    custom_settings = {
        'AUTOTHROTTLE_ENABLED': True,
        'AUTOTHROTTLE_START_DELAY': 0.5,
        'AUTOTHROTTLE_MAX_DELAY': 5,
        'AUTOTHROTTLE_TARGET_CONCURRENCY': 1.0,
        'AUTOTHROTTLE_DEBUG': False,
        'DOWNLOAD_DELAY': 1
    }

    def parse(self, response):
        target_urls = response.xpath('/html/body/div[5]/div[2]/div[1]/span[2]/div/a/@href').extract()
        subways = response.xpath('/html/body/div[5]/div[2]/div[1]/span[2]/div/a/text()').extract()
        for url, subway in zip(target_urls, subways):
            if '号线' in subway:
                yield scrapy.Request(url=url, meta={'subway': subway},
                                     callback=self.parse_base_info, headers=self.headers)

    def parse_base_info(self, response):
        subway = response.meta.get('subway')

        # 判断有没有下一页
        next_page_url = response.xpath('/html/body/div[5]/div[3]/div[3]/div/a[7]/@href').extract_first()
        if next_page_url:
            yield scrapy.Request(url=next_page_url, callback=self.parse_base_info, meta={'subway': subway},
                                 headers=self.headers)

        # 获取数据
        data_list = response.xpath('//*[@id="list-content"]/div[position()>2]')
        for data in data_list:
            item = ApmBaseInfoItem()
            item['apm_name'] = data.xpath('./div[1]/h3/a/text()').extract_first()
            item['apm_url'] = data.xpath('./div[1]/h3/a/@href').extract_first()
            item['cell_name'] = data.xpath('./div[1]/address/a/text()').extract_first()
            item['cell_type'] = data.xpath('./div[1]/p[1]/text()[1]').extract_first()
            item['area'] = data.xpath('./div[1]/p[1]/text()[2]').extract_first()
            item['built_year'] = '不知'
            item['price'] = data.xpath('./div[2]/p/strong/text()').extract_first()
            item['subway'] = subway
            item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            tracffication = data.xpath('./div[1]/p[2]/span[3]/text()').extract_first()

            # 解析租房具体信息
            meta = {
                'apm_name': item['apm_name'],
                'price': item['price'],
                'cell_type': item['cell_type'],
                'area': item['area'],
                'tracffication': tracffication,
            }
            if item['apm_url']:
                yield scrapy.Request(url=item['apm_url'], meta=meta, callback=self.parse_detail_info,
                                     headers=self.headers, dont_filter=True)

            # 返回数据
            yield item

    def parse_detail_info(self, response):
        apm_name = response.meta.get('apm_name')
        price = response.meta.get('price')
        cell_type = response.meta.get('cell_type')
        area = response.meta.get('area')
        tracffication = response.meta.get('tracffication')
        item = AmpDetailInfoItem()
        item['apm_name'] = apm_name
        item['price'] = price
        item['area'] = area
        item['apm_detail_url'] = response.url
        item['floor'] = response.xpath('/html/body/div[3]/div[2]/div[1]/ul[1]/li[5]/span[2]/text()').extract_first()
        item['traffication'] = tracffication
        item['location'] = ','.join(response.xpath('/html/body/div[3]/div[2]/div[1]/ul/li[8]/*/text()').extract()[1:-2])
        item['cell_type'] = cell_type
        item['orientation'] = response.xpath(
            '/html/body/div[3]/div[2]/div[1]/ul[1]/li[4]/span[2]/text()').extract_first()
        item['contact'] = response.xpath(
            '/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/h2/text()').extract_first()
        item['contact_identity'] = response.xpath(
            '/html/body/div[3]/div[2]/div[2]/div[1]/div[1]/div[4]/a/text()').extract_first()
        item['phone'] = '请上网查...'
        item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield item


def get_phone(data):
    """有点麻烦，先不分析了"""
    return data
