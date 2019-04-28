import re
import scrapy
from ..items import JobItem


class JobSpider(scrapy.Spider):
    name = 'jobs'
    url_temp = 'https://www.lagou.com/zhaopin/{}/'
    start_urls = (__class__.url_temp.format(i) for i in range(1, 31))

    def parse(self, response):
        print(response.url)
        for i in response.css('li.con_list_item'):
            salary = i.css('div.p_bot span::text').re('(\d+)k-(\d+)k')
            salary_list = salary if salary else [0, 0]
            experience, education = i.css('div.li_b_l::text'
                    ).extract()[2].strip().split(' / ')
            experience = re.findall('\d+', experience)
            experience_list = experience if experience else [0, 0]
            experience_list = experience if len(experience) > 1 else [0, 1]
            if len(experience) == 1:
                experience_list = [0, 1]
            yield JobItem(
                title = i.css('h3::text').extract_first(),
                city = i.xpath('.//em/text()').extract_first().split('·')[0],
                salary_low = int(salary_list[0]),
                salary_up = int(salary_list[1]),
                experience_low = int(experience_list[0]),
                experience_up = int(experience_list[1]),
                education = education,
                tags = ' '.join(i.css('div.list_item_bot span::text').extract()),
                company = i.css('div.company a::text').extract_first()
            )
