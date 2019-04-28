# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from ..db import Job, session
from .items import JobItem


class SeiyaPipeline(object):
    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            return self._process_jobitem(item)

    def _process_jobitem(self, item):
        session.add(Job(**item))

    def close_spider(self, spider):
        session.commit()
        session.close()
