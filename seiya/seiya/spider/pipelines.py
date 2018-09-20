import re

from sqlalchemy.orm import sessionmaker

from seiya.db import engine, Session, JobModel
from seiya.spider.items import JobItem


class PersistentPipeline(object):
    """持久化数据 Pipeline

    """

    def open_spider(self, spider):
        self.session = Session()

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def process_item(self, item, spider):
        if isinstance(item, JobItem):
            return self._process_job_item(item)
        else:
            return item

    def _process_job_item(self, item):
        city = item['city'].split('·')[0]

        salary_lower, salary_upper = 0, 0
        m = re.match(r'[^\d]*(\d+)k-(\d+)k', item['salary'])
        if m is not None:
            salary_lower, salary_upper = int(m.group(1)), int(m.group(2))

        experience_lower, experience_upper = 0, 0
        m = re.match(r'[^\d]*(\d+)-(\d+)', item['experience'])
        if m is not None:
            experience_lower, experience_upper = int(
                m.group(1)), int(m.group(2))

        tags = ' '.join(item['tags'])

        model = JobModel(
            title=item['title'],
            city=city,
            salary_lower=salary_lower,
            salary_upper=salary_upper,
            experience_lower=experience_lower,
            experience_upper=experience_upper,
            education=item['education'],
            tags=tags,
            company=item['company'],
        )

        self.session.add(model)

        return item
