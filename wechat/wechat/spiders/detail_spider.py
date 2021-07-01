from scrapy import Spider

from common.file_input import JsonFileInput


class WechatDetailSpider(Spider):
    name = 'wechat_detail'
    start_urls = JsonFileInput('list-res').input_result()

    def parse(self, response, **kwargs):
        pass
