from datetime import datetime
from .models import Repo, session


class HahaPipeline(object):
    def process_item(self, item, spider):
        item['update_time'] = datetime.strptime(item['update_time'], 
                              '%Y-%m-%dT%H:%M:%SZ')
        if item.get('commits'):
            item['commits'] = int(''.join(item['commits'].strip().split(',')))
            item['branches'] = int(item['branches'].strip())
            item['releases'] = int(item['releases'].strip())
        session.add(Repo(**item))
        return item

    def close_spider(self, spider):
        session.commit()
        session.close()
