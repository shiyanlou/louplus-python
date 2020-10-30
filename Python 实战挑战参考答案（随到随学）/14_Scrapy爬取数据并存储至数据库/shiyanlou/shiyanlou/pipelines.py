from sqlalchemy.orm import sessionmaker
from datetime import datetime
from .models import engine, R


class ShiyanlouPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = datetime.strptime(
            item['update_time'], 
            '%Y-%m-%dT%H:%M:%SZ')
        self.session.add(R(**item))
        return item

    def open_spider(self, spider):
        self.session = sessionmaker(engine)()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()
