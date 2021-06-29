from scrapy import Spider


class ListSpider(Spider):
    name = 'wechat_detail'
    allowed_domains = ['example.com']
    start_urls = ['http://example.com/']

    def parse(self, response):
        pass
