from scrapy import Selector
from scrapy import Spider
import re
from crawling.items import CrawlingItem
from scrapy.spiders import Rule
from scrapy.linkextractors import LinkExtractor


class ExampleSpider(Spider):
    name = 'crawling'
    allowed_domains = ['zjgj.ca']
    start_urls = ['https://www.zjgj.ca/aticle_detail2?id=2']

    def parse(self, response):
        item = CrawlingItem()
        selector = Selector(response)
        body = selector.xpath("//div[contains(@class, 'article')]")
        icons_images = body.css("img").xpath('@src').getall()

        item['body'] = body.get()
        item['title'] = selector.xpath("//div[contains(@class, 'article_title')]/h1[1]/text()").get()
        item['localtime'] = selector.xpath("//div[contains(@class, 'article_time')]/span/text()").get()
        item['images'] = [img for img in icons_images if re.match('http://xy-hzj.oss-cn-shanghai.aliyuncs.com',img)]
        yield item
