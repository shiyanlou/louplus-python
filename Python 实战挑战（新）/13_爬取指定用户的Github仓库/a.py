import scrapy

class S(scrapy.Spider):
    name = 's'
    url = 'https://github.com/shiyanlou?page={}&tab=repositories'
    start_urls = (__class__.url.format(i) for i in range(1, 5))

    def parse(self, r):
        for i in r.css('li.col-12'):
            yield {
                'name': i.css('a::text').extract_first().strip(),
                'update_time': i.css('relative-time::attr(datetime)').extract_first()
            }
