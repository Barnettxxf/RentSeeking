# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ApmBaseInfoItem(scrapy.Item):
    apm_name = scrapy.Field()
    apm_url = scrapy.Field()
    cell_name = scrapy.Field()
    cell_type = scrapy.Field()
    area = scrapy.Field()
    built_year = scrapy.Field()
    price = scrapy.Field()
    subway = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()


class AmpDetailInfoItem(scrapy.Item):
    apm_name = scrapy.Field()
    price = scrapy.Field()
    area = scrapy.Field()
    floor = scrapy.Field()
    apm_detail_url = scrapy.Field()
    traffication = scrapy.Field()
    location = scrapy.Field()
    cell_type = scrapy.Field()
    orientation = scrapy.Field()
    contact = scrapy.Field()
    contact_identity = scrapy.Field()
    phone = scrapy.Field()
    created_at = scrapy.Field()
    updated_at = scrapy.Field()