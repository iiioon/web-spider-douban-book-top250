import requests
from lxml import etree
from fake_useragent import UserAgent
import time
import random


class DoubanBookSpider:
    def __init__(self):
        self.url = 'http://book.douban.com/top250?start={}'

    def get_html(self, url):
        headers = {'User-Agent': UserAgent().random}
        html = requests.get(url=url, headers=headers).text
        self.parse_html(html)

    def parse_html(self, html):
        parse_obj = etree.HTML(html)
        table_list = parse_obj.xpath('.//div[@class="indent"]/table')
        for table in table_list:
            item = {}
            name_list = table.xpath('.//div[@class="pl2"]/a/@title')
            item['name'] = name_list[0].strip() if name_list else None
            content_list = table.xpath('.//p[@class="pl"]/text()')
            item['content'] = content_list[0].strip() if content_list else None
            score_list = table.xpath('.//span[@class="rating_nums"]/text()')
            item['score'] = score_list[0].strip() if score_list else None
            nums_list = table.xpath('.//span[@class="pl"]/text()')
            item['nums'] = nums_list[0][1:-1].strip() if nums_list else None
            type_list = table.xpath('.//span[@class="inq"]/text()')
            item['type'] = type_list[0].strip() if type_list else None
            print(item)

    def run(self):
        for i in range(5):
            start = (i - 1) * 25
            page_url = self.url.format(start)
            self.get_html(page_url)
            time.sleep(random.randint(1, 2))


if __name__ == '__main__':
    spider = DoubanBookSpider()
    spider.run()
