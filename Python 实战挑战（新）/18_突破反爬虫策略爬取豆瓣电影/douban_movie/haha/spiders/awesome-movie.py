# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from haha.items import HahaItem


class DoubanSpider(CrawlSpider):
    name = 'douban'
    start_urls = ['https://movie.douban.com/subject/3011091/']

    rules = (
        Rule(LinkExtractor(allow='https://movie.douban.com/subject/\d+/\?'
            'from=subject-page'), callback='parse_item', follow=1),
    )

    def parse_item(self, response):
        # 如果需要打印用户代理以查看其是否随机变化，使用下一行代码
        #print(response.request.headers.get('User-Agent'))
        return HahaItem({
            'url': response.url,
            'name': response.xpath('//span[@property="v:itemreviewed"]/text()').extract_first(),
            'summary': response.xpath('//span[@property="v:summary"]/text()').extract_first(),
            'score': response.xpath('//strong[@property="v:average"]/text()').extract_first()
        })

    # 以上代码可以完成爬取任务，注意这里不允许定义 parse 方法
    # 但 start_urls 地址将不会被爬取数据，仅从中获得符合规则的链接
    # 若想爬取 start_urls 的数据，取消下面两行代码的注释即可

    #def parse_start_url(self, response):  # 注意这个方法的名字是固定的
    #    yield self.parse_item(response)
