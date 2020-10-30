import scrapy

class CoursesSpider(scrapy.Spider):
    name = 'courses'

    start_urls = ['https://www.shiyanlou.com/bootcamp/']

    def parse(self, response):
        for course in response.css('div.bootcamp-courses-item'):
            yield {
                'name': course.xpath('.//div[@class="course-title"]/a/span/text()').extract_first().strip(),
                'description': course.xpath('.//div[@class="course-desc"]/a/p/text()').extract_first().strip(),
                'image_url': course.xpath('.//div[@class="course-img"]/a/img/@src').extract_first()
            }
