# -*- coding:utf-8 -*-

import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from RentSeeking.spiders.anjuke import AnjukeSpider
from RentSeeking.spiders.lianjia import LianjiaSpider

settings = get_project_settings()
process = CrawlerProcess(settings=settings)
process.crawl(AnjukeSpider)
process.crawl(LianjiaSpider)
process.start()
