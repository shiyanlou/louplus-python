import json

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from scrapy.http import HtmlResponse


results = []


def parse(response):
    for comment in response.css('div.comment-list-item'):
        result = dict(
            username=comment.xpath(
                './/a[@class="username"]/text()').extract_first().strip(),
            content=comment.xpath(
                './/div[contains(@class, "comment-item-content")]/p/text()').extract_first()
        )
        print("comment: {}".format(result))
        results.append(result)


def has_next_page(response):
    classes = response.xpath(
        '//li[contains(@class, "next-page")]/@class').extract_first()
    return 'disabled' not in classes


def goto_next_page(driver):
    next_page_btn = driver.find_element_by_xpath(
        '//li[contains(@class, "next-page")]')
    next_page_btn.click()


def wait_page_return(driver, page):
    WebDriverWait(driver, 10).until(
        EC.text_to_be_present_in_element(
            (By.XPATH, '//ul[@class="pagination"]/li[@class="active"]'),
            str(page)
        )
    )


def spider():
    # 如果本地有安装 Chrome 浏览器，推荐使用 Chrome WebDriver，PhantomJS WebDriver 即将被 Selenium 废弃
    driver = webdriver.PhantomJS()
    url = 'https://www.shiyanlou.com/courses/427'
    driver.get(url)
    page = 1
    while True:
        print("crawl page {}".format(page))
        wait_page_return(driver, page)
        html = driver.page_source
        response = HtmlResponse(url=url, body=html.encode('utf8'))
        parse(response)
        if not has_next_page(response):
            break
        page += 1
        goto_next_page(driver)
    with open('comments.json', 'w') as f:
        f.write(json.dumps(results))


if __name__ == '__main__':
    spider()
