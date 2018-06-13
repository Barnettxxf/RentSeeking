# -*- coding: utf-8 -*-
import datetime
import scrapy

from urllib.parse import urljoin, urlsplit
from RentSeeking.items import ApmBaseInfoItem, AmpDetailInfoItem
import re


class LeyoujiaSpider(scrapy.Spider):
    name = 'leyoujia'
    allowed_domains = ['shenzhen.leyoujia.com']
    start_urls = ['https://shenzhen.leyoujia.com/zf/ditie/']
    headers = {

    }

    def parse(self, response):
        target_urls = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/div[1]/a/@href').extract()
        subways = response.xpath('/html/body/div[3]/div[1]/div[1]/div[2]/div[1]/a/text()').extract()
        subways = [x.strip() for x in subways]
        for url, subway in zip(target_urls, subways):
            if '号线' in subway:
                yield scrapy.Request(url=urljoin(self.start_urls[-1], url), meta={'subway': subway},
                                     callback=self.parse_base_info, headers=self.headers)

    def parse_base_info(self, response):
        subway = response.meta.get('subway')

        # 判断有没有下一页
        next_page_urls = response.xpath('/html/body/div[3]/div[3]/div[1]/div[3]/div/div/a/@href').extract()
        next_page_texts = response.xpath('/html/body/div[3]/div[3]/div[1]/div[3]/div/div/a/text()').extract()
        for url, text in zip(next_page_urls, next_page_texts):
            if '下一页' not in text.strip():
                next_page_url = urljoin(self.start_urls[-1], url)
                yield scrapy.Request(url=next_page_url, callback=self.parse_base_info,
                                     meta={'subway': subway}, headers=self.headers)

        # 获取数据
        data_list = response.xpath('/html/body/div[3]/div[3]/div[1]/div[3]/ul/li')
        for data in data_list:
            item = ApmBaseInfoItem()
            item['apm_name'] = data.xpath('./div[2]/p[1]/a/text()').extract_first()
            item['apm_url'] = data.xpath('./div[2]/p[1]/a/@href').extract_first()
            item['apm_url'] = urljoin(self.start_urls[-1], item['apm_url'])
            item['cell_name'] = data.xpath('./div[2]/p[4]/span[1]/a/text()').extract_first()
            item['cell_type'] = data.xpath('./div[2]/p[2]/span[1]/text()').extract_first()
            item['area'] = data.xpath('./div[2]/p[2]/span[4]/text()').extract_first()
            if item['area']:
                item['area'] = re.search('\d+', item['area']).group()
            item['built_year'] = data.xpath('./div[2]/p[3]/span[3]/text()').extract_first()
            item['price'] = data.xpath('./div[3]/p[1]/span/text()').extract_first()
            item['subway'] = subway
            item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # 解析租房具体信息
            meta = {
                'apm_name': item['apm_name'],
                'price': item['price'],
                'cell_type': item['cell_type'],
                'area': item['area'],
                'subway': subway,
            }
            yield scrapy.Request(url=item['apm_url'], meta=meta, callback=self.parse_detail_info,
                                 headers=self.headers)
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
        item['floor'] = response.xpath('*//div[@class="intro-box6 clearfix"]/span[1]/text()').extract_first()
        item['traffication'] = subway
        item['location'] = response.xpath('*//span[@class="location mr10 fl"]/text()').extract_first()
        item['cell_type'] = cell_type
        item['orientation'] = response.xpath('//*[@id="fyjs"]/div/div[1]/div/span[4]/em/text()').extract_first()
        item['contact'] = response.xpath('*//span[@class="name"]/text()').extract_first()
        item['contact_identity'] = '不详'
        item['phone'] = response.xpath('*//span[@class="telnum"]/text()').extract_first()
        item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield item
