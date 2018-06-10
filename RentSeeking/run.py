# -*- coding:utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from .spiders.anjuke import AnjukeSpider
from .spiders.lianjia import LianjiaSpider

process = CrawlerProcess()
process.crawl(AnjukeSpider)
process.crawl(LianjiaSpider)
process.start()
