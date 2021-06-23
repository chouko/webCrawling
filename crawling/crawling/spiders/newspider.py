import re

from scrapy import Selector
from scrapy import Spider
from scrapy import Request
from crawling.items import CrawlingItem

TYPE_CATEGORY = {1: "小学至高中留学",
                 2: "大学及社区学院",
                 3: "加拿大移民优势",
                 4: "加拿大移民项目",
                 5: "新生活新常识",
                 6: "时事新闻"}
START_URLS = ['https://www.zjgj.ca/action?type=1',
              'https://www.zjgj.ca/action?type=2',
              'https://www.zjgj.ca/action?type=3',
              'https://www.zjgj.ca/action?type=4',
              'https://www.zjgj.ca/action?type=5',
              'https://www.zjgj.ca/action?type=6']

DOMAINS = ['zjgj.ca']


class NewsSpider(Spider):
    name = 'crawling'
    allowed_domains = DOMAINS
    start_urls = ['https://www.zjgj.ca/aticle_detail2?id=10000']
                  # 'https://www.zjgj.ca/aticle_detail2?id=10001',
                  # 'https://www.zjgj.ca/aticle_detail2?id=10002']
    # start_urls = START_URLS

    def parse(self, response):
        item = CrawlingItem()
        selector = Selector(response)
        body = selector.xpath("//div[contains(@class, 'article')]")
        icons_images = body.css("img").xpath('@src').getall()
        news_links = selector.xpath("//div[contains(@class, 'article')]")

        item['source_url'] = 'https://www.zjgj.ca/aticle_detail2?id=10000'
        item['body'] = body.get()
        item['title'] = selector.xpath("//div[contains(@class, 'article_title')]/h1[1]/text()").get()
        item['localtime'] = selector.xpath("//div[contains(@class, 'article_time')]/span/text()").get()
        item['image_urls'] = set([img for img in icons_images if re.match('^(http)', img)])
        item['category'] = [TYPE_CATEGORY[1]]
        yield item

    def manual_callback_parse(self, response):
        yield Request('')
