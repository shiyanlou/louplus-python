# -*- coding: utf-8 -*-
import scrapy


class RestaurantsSpider(scrapy.Spider):
    name = 'restaurants'
    allowed_domains = ['www.dianping.com']
    start_urls = ['http://www.dianping.com/']

    def parse(self, response):
        pass
