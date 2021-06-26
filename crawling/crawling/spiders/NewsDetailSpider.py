import re

from scrapy import Spider, Selector

from crawling.constant_settings import HTML, HEAD, BODY, KEY_WORD
from crawling.items import CrawlingItem


class DetailSpider(Spider):
    name = 'news_detail'
    allowed_domains = ['www.zjgj.ca']

    start_urls = ['https://www.zjgj.ca/aticle_detail2?id=5'
        , 'https://www.zjgj.ca/aticle_detail2?id=25']

    def parse(self, response):
        item = CrawlingItem()
        selector = Selector(response)
        body = selector.xpath("//div[contains(@class, 'article')]")
        icons_images = body.css("img").xpath('@src').getall()

        item['body'] = HTML % (HEAD, (BODY % body.get()))
        item['title'] = selector.xpath("//div[contains(@class, 'article_title')]/h1[1]/text()").get()
        item['localtime'] = selector.xpath("//div[contains(@class, 'article_time')]/span/text()").get()
        item['image_urls'] = set([img for img in icons_images if re.match(r'^[^(http)]', img)])
        item['category'] = 'PRODUCT' if True in [word in item['title'] for word in KEY_WORD] else 'NEWS'
        item['summary'] = body
        item['resource_links'] = set([link for link in (selector.xpath("//link/@href | //script/@src").getall())
                                      if re.match(r'^[^(http)]', link)])

        yield item
