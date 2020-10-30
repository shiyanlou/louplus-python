import scrapy

class ShiyanlouItem(scrapy.Item):
    name = scrapy.Field()
    update_time = scrapy.Field()
