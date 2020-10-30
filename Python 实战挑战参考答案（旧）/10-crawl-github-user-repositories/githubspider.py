# -*- coding: utf-8 -*-
import scrapy


class GithubSpider(scrapy.Spider):
    name = 'shiyanlou-github'

    @property
    def start_urls(self):
        return ('https://github.com/shiyanlou?tab=repositories', )

    def parse(self, response):
        for repository in response.css('li.public'):
            yield {
                'name': repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first(r'\n\s*(.*)'),
                'update_time': repository.xpath('.//relative-time/@datetime').extract_first()
            }
