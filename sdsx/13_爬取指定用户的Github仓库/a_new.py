import scrapy

class Github(scrapy.Spider):
    name = 'xxx'
    start_urls = [
        'https://github.com/shiyanlou?tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wNlQxNzozNjoxNSswODowMM4FkpW2&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yM1QxNDoxODoyMSswODowMM4By2VI&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0xOVQxMDoxMDoyMyswODowMM4BmcsV&tab=repositories'
    ]

    def parse(self, response):
        for i in response.css('li.col-12'):
            yield {
                'name': i.xpath('.//a/text()').extract_first().strip(),
                'update_time': i.xpath('.//relative-time/@datetime').extract_first()
            }
