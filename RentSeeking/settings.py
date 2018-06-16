# -*- coding: utf-8 -*-

# Scrapy settings for RentSeeking project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://doc.scrapy.org/en/latest/topics/settings.html
#     https://doc.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://doc.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'RentSeeking'

SPIDER_MODULES = ['RentSeeking.spiders']
NEWSPIDER_MODULE = 'RentSeeking.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

CONCURRENT_REQUESTS = 32

# DOWNLOAD_DELAY = 2
CONCURRENT_REQUESTS_PER_DOMAIN = 16
CONCURRENT_REQUESTS_PER_IP = 16

DEFAULT_REQUEST_HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.19 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Upgrade-Insecure-Requests': '1',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}

# Disable cookies (enabled by default)
COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
# TELNETCONSOLE_ENABLED = False

# Override the default request headers:
# DEFAULT_REQUEST_HEADERS = {
#   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
#   'Accept-Language': 'en',
# }

# Enable or disable spider middlewares
# See https://doc.scrapy.org/en/latest/topics/spider-middleware.html
# SPIDER_MIDDLEWARES = {
#    'RentSeeking.middlewares.RentseekingSpiderMiddleware': 543,
# }
# {
#     'scrapy.contrib.downloadermiddleware.robotstxt.RobotsTxtMiddleware': 100,
#     'scrapy.contrib.downloadermiddleware.httpauth.HttpAuthMiddleware': 300,
#     'scrapy.contrib.downloadermiddleware.downloadtimeout.DownloadTimeoutMiddleware': 350,
#     'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': 400,
#     'scrapy.contrib.downloadermiddleware.retry.RetryMiddleware': 500,
#     'scrapy.contrib.downloadermiddleware.defaultheaders.DefaultHeadersMiddleware': 550,
#     'scrapy.contrib.downloadermiddleware.redirect.MetaRefreshMiddleware': 580,
#     'scrapy.contrib.downloadermiddleware.httpcompression.HttpCompressionMiddleware': 590,
#     'scrapy.contrib.downloadermiddleware.redirect.RedirectMiddleware': 600,
#     'scrapy.contrib.downloadermiddleware.cookies.CookiesMiddleware': 700,
#     'scrapy.contrib.downloadermiddleware.httpproxy.HttpProxyMiddleware': 750,
#     'scrapy.contrib.downloadermiddleware.chunked.ChunkedTransferMiddleware': 830,
#     'scrapy.contrib.downloadermiddleware.stats.DownloaderStats': 850,
#     'scrapy.contrib.downloadermiddleware.httpcache.HttpCacheMiddleware': 900,
# }
# HTTPERROR_ALLOWED_CODES = [403, 302]
RETRY_HTTP_CODES = [500, 502, 503, 504, 400, 408, 403, 302]
RETRY_TIMES = 3

DOWNLOADER_MIDDLEWARES = {
    'scrapy.contrib.downloadermiddleware.useragent.UserAgentMiddleware': None,
    'RentSeeking.middlewares.RotateUserAgentMiddleware': 400,
    'RentSeeking.middlewares.RentSeekingDownloaderMiddleware': 544,
}

ITEM_PIPELINES = {
    'RentSeeking.pipelines.RentseekingPipeline': 300,
    'RentSeeking.pipelines.MysqlPipline': 301,
}

# AUTOTHROTTLE_ENABLED = True
# AUTOTHROTTLE_START_DELAY = .5
# AUTOTHROTTLE_MAX_DELAY = 1.5
# AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# AUTOTHROTTLE_DEBUG = True
