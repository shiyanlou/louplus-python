# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import ShiyanlouItem

class ReSpider(scrapy.Spider):
    name = 're'
    url = 'https://github.com/shiyanlou?page={}&tab=repositories'
    start_urls = (__class__.url.format(i) for i in range(1, 5))

    def parse(self, response):
        for i in response.css('li.col-12'):
            yield ShiyanlouItem({
                'name': i.css('a::text').extract_first().strip(),
                'update_time': i.css('relative-time::attr(datetime)').extract_first()
            })
