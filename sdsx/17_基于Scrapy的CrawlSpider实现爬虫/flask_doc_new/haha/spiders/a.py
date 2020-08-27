import scrapy
from scrapy.spiders import Rule, CrawlSpider
from scrapy.linkextractors import LinkExtractor
from ..items import HahaItem

class Haha(CrawlSpider):
    name = 'haha'
    start_urls = ['https://flask.palletsprojects.com/en/1.0.x/']
    rules = (
        Rule(
            LinkExtractor(allow='https://flask.palletsprojects.com/en/1.0.x/*'),
            callback='parse_item',
            follow=True
        ),
    )

    def parse_item(self, response):
        yield HahaItem(
            url = response.url,
            text = ' '.join(response.css('::text').extract())
        )
