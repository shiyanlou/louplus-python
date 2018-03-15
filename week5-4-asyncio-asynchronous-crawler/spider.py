import csv
import asyncio
import aiohttp
import async_timeout
from scrapy.http import HtmlResponse


results = []


async def fetch(session, url):
    with async_timeout.timeout(10):
        async with session.get(url) as response:
            return await response.text()


def parse(url, body):
    response = HtmlResponse(url=url, body=body)
    for repository in response.css('li.public'):
        name = repository.xpath('.//a[@itemprop="name codeRepository"]/text()').re_first("\n\s*(.*)")
        update_time = repository.xpath('.//relative-time/@datetime').extract_first()
        results.append((name, update_time))


async def task(url):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, url)
        parse(url, html.encode('utf-8'))


def main():
    loop = asyncio.get_event_loop()
    url_template = 'https://github.com/shiyanlou?page={}&tab=repositories'
    tasks = [task(url_template.format(i)) for i in range(1, 5)]
    loop.run_until_complete(asyncio.gather(*tasks))
    with open('shiyanlou-repos.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)


if __name__ == '__main__':
    main()
