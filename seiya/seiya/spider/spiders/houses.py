# -*- coding: utf-8 -*-
import scrapy


class HousesSpider(scrapy.Spider):
    name = 'houses'
    allowed_domains = ['cd.lianjia.com']
    start_urls = ['http://cd.lianjia.com/']

    def parse(self, response):
        pass
