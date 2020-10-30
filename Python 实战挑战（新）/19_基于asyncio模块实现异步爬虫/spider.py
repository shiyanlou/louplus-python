import csv
import asyncio
import aiohttp
from scrapy.http import HtmlResponse


results = []


def parse(url, body):
    response = HtmlResponse(url=url, body=body)
    for repository in response.css('li.public'):
        name = repository.xpath('.//a[@itemprop="name codeRepository"]/text()'
                ).re_first(r"\n\s*(.*)")
        update_time = repository.xpath('.//relative-time/@datetime'
                ).extract_first()
        results.append((name, update_time))


async def task(url):
    timeout = aiohttp.client.ClientTimeout(total=10)
    user_agent = ('Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) '
            'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 '
            'Safari/537.36')
    headers = {'User-Agent': user_agent}
    async with aiohttp.ClientSession(timeout=timeout) as session:
        async with session.get(url, headers=headers, verify_ssl=False) as resp:
            html = await resp.text()
            parse(url, html.encode('utf-8'))


def main():
    loop = asyncio.get_event_loop()
    urls = (
        'https://github.com/shiyanlou?tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNy0wNi0wN' + \
                '1QwNjoxOTo1NyswODowMM4FkpYw&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNS0wMS0yN' + \
                'VQxMTozMTowNyswODowMM4Bxrsx&tab=repositories',
        'https://github.com/shiyanlou?after=Y3Vyc29yOnYyOpK5MjAxNC0xMS0yM' + \
                'FQxMzowMzo1MiswODowMM4BjkvL&tab=repositories'
    )
    tasks = [task(url) for url in urls]
    loop.run_until_complete(asyncio.gather(*tasks))
    with open('shiyanlou-repos.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(results)


if __name__ == '__main__':
    main()
