import scrapy
from ..items import HahaItem


class GithubSpider(scrapy.Spider):
    name = 'github'
    start_urls = ['https://github.com/shiyanlou?tab=repositories']

    def parse(self, response):
        for i in response.css('li.col-12'):
            item = HahaItem()
            item['name'] = i.css('a::text').extract_first().strip()
            item['update_time'] = i.xpath('.//relative-time/@datetime').extract_first()
            url = i.xpath('.//h3/a/@href').extract_first()
            request = scrapy.Request(response.urljoin(url), self.parse_repo)
            request.meta['item'] = item
            yield request
        url = response.css('div.BtnGroup a::attr(href)').extract()[-1]
        yield response.follow(url, self.parse)

    def parse_repo(self, response):
        item = response.meta['item']
        br = response.css('div.ml-3 strong::text').extract()
        if br:
            item['branches'] = br[0]
            item['releases'] = br[1]
            item['commits'] = response.css('li.ml-0 strong::text').extract_first()
        return item
