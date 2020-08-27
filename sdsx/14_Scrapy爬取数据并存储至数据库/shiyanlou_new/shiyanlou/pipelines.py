# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from .items import ShiyanlouItem
from .models import Repository, session

class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = datetime.strptime(
            item['update_time'], '%Y-%m-%dT%H:%M:%SZ')
        session.add(Repository(**item))
        return item

    def close_spider(self, spider):
        session.commit()
        session.close()
