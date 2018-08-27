import scrapy


class JobItem(scrapy.Item):
    title = scrapy.Field()
    city = scrapy.Field()
    salary = scrapy.Field()
    experience = scrapy.Field()
    education = scrapy.Field()
    tags = scrapy.Field()
    company = scrapy.Field()
