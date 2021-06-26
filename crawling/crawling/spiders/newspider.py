import re

from scrapy import Selector
from scrapy import Spider
from scrapy import Request
from crawling.constant_settings import HOST, START_URLS, DETAIL_PATTERN, NEXT_PAGE_XPATH, FINAL_PAGE_XPATH, \
    DOMAIN, HTML, HEAD, BODY, KEY_WORD

# TYPE_CATEGORY = {1: "小学至高中留学",
#                  2: "大学及社区学院"
#                  3: "加拿大移民优势",
#                  4: "加拿大移民项目",
#                  5: "新生活新常识",
#                  6: "时事新闻"}

from crawling.items import CrawlingItem


class NewsSpider(Spider):
    name = 'news_list_detail'
    allowed_domains = [HOST]

    start_urls = START_URLS

    def parse(self, response):
        selector = Selector(response)
        try:
            articles = selector.xpath(DETAIL_PATTERN)
            next_link = selector.xpath(NEXT_PAGE_XPATH).get()
            final_link = selector.xpath(FINAL_PAGE_XPATH).get()
            for article in articles:
                yield Request(DOMAIN + article.xpath("@href").get(),
                              callback=self.parse_detail,
                              cb_kwargs=dict(summary=article.xpath(".//p[contains(@class,"
                                                                   "'lines-limit-length')]/text()").get()),
                              errback=self.errback)

            if int(next_link.split('=')[-1]) < int(final_link.split('=')[-1]):
                yield Request(DOMAIN + next_link, callback=self.parse, errback=self.errback)
        except IndexError:
            pass

    def parse_detail(self, response, summary=None):
        item = CrawlingItem()
        selector = Selector(response)
        body = selector.xpath("//div[contains(@class, 'article')]")
        icons_images = body.css("img").xpath('@src').getall()

        item['body'] = HTML % (HEAD, (BODY % body.get()))
        item['title'] = selector.xpath("//div[contains(@class, 'article_title')]/h1[1]/text()").get()
        item['localtime'] = selector.xpath("//div[contains(@class, 'article_time')]/span/text()").get()
        item['image_urls'] = set([img for img in icons_images if re.match(r'^[^(http)]', img)])
        item['category'] = 'PRODUCT' if True in [word in item['title'] for word in KEY_WORD] else 'NEWS'
        item['summary'] = summary
        item['resource_links'] = set([link for link in (selector.xpath("//link/@href | //script/@src").getall())
                                      if re.match(r'^[^(http)]', link)])
        yield item

    def errback(self, failure):
        self.logger.error(repr(failure))
