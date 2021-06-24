import re

from scrapy import Selector
from scrapy import Spider
from scrapy import Request
from crawling.items import CrawlingItem
from scrapy.linkextractors import LinkExtractor

# TYPE_CATEGORY = {1: "小学至高中留学",
#                  2: "大学及社区学院",
#                  3: "加拿大移民优势",
#                  4: "加拿大移民项目",
#                  5: "新生活新常识",
#                  6: "时事新闻"}
START_URLS = ['https://www.zjgj.ca/action?pageNum=1']

DOMAINS = ['zjgj.ca']

DETAIL_PATTERN = "//div[contains(@class,media item)]"
NEXT_PAGE_XPATH = "//'ul'[contains(@class,'pagingArea')]/li/a[2]/@href"
FINAL_PAGE_XPATH = "//ul[contains(@class,'pagingArea')]/li/a[3]/@href"


class NewsSpider(Spider):
    name = 'crawling'
    allowed_domains = DOMAINS

    start_urls = START_URLS

    def parse(self, response):
        selector = Selector(response)
        try:
            articles = selector.xpath(DETAIL_PATTERN).getall()
            next_link = selector.xpath(NEXT_PAGE_XPATH)
            final_link = selector.xpath(FINAL_PAGE_XPATH)
            for article in articles:
                yield Request(article.xpath("//a/@href"),
                              callback=self.parse_detail(response, article.xpath("//a/p/text()").get()))

            if next_link.split('=')[-1] < final_link.split('=')[-1]:
                yield Request(next_link)
        except IndexError:
            pass

    def parse_detail(self, response, summary=None):
        item = CrawlingItem()
        selector = Selector(response)
        body = selector.xpath("//div[contains(@class, 'article')]")
        icons_images = body.css("img").xpath('@src').getall()

        item['body'] = body.get()
        item['title'] = selector.xpath("//div[contains(@class, 'article_title')]/h1[1]/text()").get()
        item['localtime'] = selector.xpath("//div[contains(@class, 'article_time')]/span/text()").get()
        item['image_urls'] = set([img for img in icons_images if re.match('^(http)', img)])
        item['category'] = 'NEWS'
        item['summary'] = summary
        yield item
