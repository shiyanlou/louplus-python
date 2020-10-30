# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json, redis, re

class HahaPipeline(object):
    def process_item(self, item, spider):
        item['text'] = re.sub('\s+', ' ', item['text'])
        self.redis.lpush('flask_doc:items', json.dumps(dict(item)))
        return item

    def open_spider(self, spider):
        self.redis = redis.Redis(
            host='localhost', 
            port=6379, 
            decode_responses=True
        )
