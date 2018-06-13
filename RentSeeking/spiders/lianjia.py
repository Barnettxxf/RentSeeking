# -*- coding: utf-8 -*-
import datetime
import scrapy
from urllib.parse import urljoin, urlsplit
from RentSeeking.items import ApmBaseInfoItem, AmpDetailInfoItem
import re


class LianjiaSpider(scrapy.Spider):
    name = 'lianjia'
    allowed_domains = ['sz.lianjia.com']
    start_urls = ['https://sz.lianjia.com/ditiezufang/']
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.19 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Upgrade-Insecure-Requests': '1',
        'Accept-Language': 'zh-CN,zh;q=0.9',
    }

    def parse(self, response):
        target_urls = response.xpath('//*[@id="filter-options"]/dl[1]/dd/div/a/@href').extract()
        subways = response.xpath('//*[@id="filter-options"]/dl[1]/dd/div/a/text()').extract()
        for url, subway in zip(target_urls, subways):
            if '号线' in subway:
                yield scrapy.Request(url=urljoin(self.start_urls[-1], url), meta={'subway': subway},
                                     callback=self.parse_base_info, headers=self.headers)

    def parse_base_info(self, response):
        subway = response.meta.get('subway')
        total_page = response.meta.get('total_page')
        current_page = re.search('"curPage":(\d+)', response.text).group(1)
        # 判断有没有下一页
        if total_page is None:
            total_page = re.search('"totalPage":(\d+)', response.text).group(1)

        next_page = int(current_page) + 1
        if 'pg%s' % current_page not in response.url:
            url = urljoin(response.url, 'pg%s' % current_page)
        else:
            url = None

        if url is None:
            url = response.url.replace('pg%s' % current_page, 'pg%d' % next_page)
        else:
            url = url.replace('pg%s' % current_page, 'pg%d' % next_page)

        if int(current_page) < int(total_page):
            yield scrapy.Request(url=url, callback=self.parse_base_info,
                                 meta={'subway': subway, 'total_page': total_page}, headers=self.headers)

        # 获取数据
        data_list = response.xpath('//*[@id="house-lst"]/li')
        for data in data_list:
            item = ApmBaseInfoItem()
            item['apm_name'] = data.xpath('./div[2]/h2/a/text()').extract_first()
            item['apm_url'] = data.xpath('./div[2]/h2/a/@href').extract_first()
            item['cell_name'] = data.xpath('./div[2]/div[1]/div[1]/a/span/text()').extract_first()
            item['cell_type'] = data.xpath('./div[2]/div[1]/div[1]/span[1]/span/text()').extract_first()
            item['area'] = data.xpath('./div[2]/div[1]/div[1]/span[2]/text()').extract_first().strip()
            item['built_year'] = data.xpath('./div[2]/div[1]/div[2]/div/text()[2]').extract_first()
            item['price'] = data.xpath('./div[2]/div[2]/div[1]/span/text()').extract_first()
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
            yield scrapy.Request(url=item['apm_url'], meta=meta, callback=self.parse_detail_info, headers=self.headers)
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
        item['floor'] = response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[3]/text()').extract_first()
        item['traffication'] = response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[5]/text()').extract_first()
        item['location'] = ','.join(
            response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[7]/*/text()').extract()[1:])
        item['cell_type'] = cell_type
        item['orientation'] = response.xpath('/html/body/div[4]/div[2]/div[2]/div[2]/p[4]/text()').extract_first()
        item['contact'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[3]/div/div[1]/a[1]/text()').extract_first()
        item['contact_identity'] = response.xpath(
            '/html/body/div[4]/div[2]/div[2]/div[3]/div/div[1]/span/text()').extract_first()
        item['phone'] = ','.join(
            [x.strip() for x in response.xpath('/html/body/div[4]/div[2]/div[2]/div[3]/div/div[3]/text()').extract()])
        item['created_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        item['updated_at'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        yield item
