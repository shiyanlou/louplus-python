# -*- coding: utf-8 -*-
import scrapy
from ..items import ShiyanlouItem


class HahaSpider(scrapy.Spider):
    name = 'haha'
    allowed_domains = ['github.com']
    start_urls = [ 
        'https://github.com/shiyanlou?tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjoxNSswODowMM4FkpW2&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yM1QxNDoxODoyMSswODowMM4By2VI&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0xOVQxMDoxMDoyMyswODowMM4BmcsV&tab=repositories'
    ]   

    def parse(self, response):
        for i in response.xpath('//li[contains(@class, "col-12")]'):
            yield ShiyanlouItem(
                name = i.xpath('.//a/text()').extract_first().strip(),
                update_time = i.xpath('.//relative-time/@datetime').extract_first()
            )
