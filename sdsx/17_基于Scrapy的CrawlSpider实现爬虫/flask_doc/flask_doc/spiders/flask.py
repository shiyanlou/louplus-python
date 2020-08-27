# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from flask_doc.items import HahaItem

class FlaskSpider(CrawlSpider):
    name = 'flask'
    start_urls = ['http://flask.pocoo.org/docs/0.12/']

    rules = (
        Rule(LinkExtractor(allow='http://flask.pocoo.org/docs/0.12/.*'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        yield HahaItem({
            'url': response.url,
            'text': ' '.join(response.css('::text').extract())
        })
