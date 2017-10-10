# -*- coding: utf-8 -*-
import scrapy
from shiyanlou.items import GithubItem

class GithubSpider(scrapy.Spider):
    name = 'github'
    allowed_domains = ['github.com']

    @property
    def start_urls(self):
        url_tmpl = 'https://github.com/shiyanlou?page={}&tab=repositories'
        return (url_tmpl.format(i) for i in range(1, 5))

    def parse(self, response):
        for repository in response.css('li.public'):
            item = GithubItem()
            item['name'] = repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)")
            item['update_time'] = repository.xpath('.//relative-time/@datetime').extract_first() 
            repo_url = response.urljoin(repository.xpath('.//a/@href').extract_first())
            request = scrapy.Request(repo_url, callback=self.parse_repo)
            request.meta['item'] = item
            yield request

    def parse_repo(self, response):
        item = response.meta['item']
        for number in response.css('ul.numbers-summary li'):
            type_text = number.xpath('.//a/text()').re_first('\n\s*(.*)\n')
            number_text = number.xpath('.//span[@class="num text-emphasized"]/text()').re_first('\n\s*(.*)\n')
            if type_text and number_text:
                number_text = number_text.replace(',','')
                if type_text in ('commit', 'commits'):
                    item['commits'] = int(number_text)
                elif type_text in ('branch', 'branches'):
                    item['branches'] = int(number_text)
                elif type_text in ('release', 'releases'):
                    item['releases'] = int(number_text)
        yield item

