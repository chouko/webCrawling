import re

from scrapy import Spider, Selector

from crawling.items import CrawlingItem


class DetailSpider(Spider):
    name = 'news_detail'
    allowed_domains = ['www.zjgj.ca']

    start_urls = ['https://www.zjgj.ca/aticle_detail2?id=65']

    def parse(self, response):
        item = CrawlingItem()
        selector = Selector(response)
        body = selector.xpath("//div[contains(@class, 'article')]")
        icons_images = body.css("img").xpath('@src').getall()

        item['body'] = selector.get()  # 整段html
        item['title'] = selector.xpath("//div[contains(@class, 'article_title')]/h1[1]/text()").get()
        item['localtime'] = selector.xpath("//div[contains(@class, 'article_time')]/span/text()").get()
        item['image_urls'] = set([img for img in icons_images if re.match(r'^[^(http)]', img)])
        item['category'] = 'NEWS'
        item['summary'] = ''
        item['resource_links'] = set([link for link in (selector.xpath("//link/@href | //script/@src").getall())
                                      if re.match(r'^[^(http)]', link)])
        yield item
