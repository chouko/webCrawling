from bs4 import BeautifulSoup
from scrapy import Spider, Selector, Request

from common.file_input import JsonFileInput
from wechat.items import WechatDetailItem


class WechatDetailSpider(Spider):
    name = 'wechat_detail'

    def start_requests(self):
        i = 0
        _input = JsonFileInput('list-res').input_result()
        for req in [data["link"] for data in _input]:
            # yield Request(req, callback=self.parse, )
            i += 1
            yield Request('http://mp.weixin.qq.com/s?__biz=MzA4NDg0NzYyMg==&mid=2651711890&idx=1&sn'
                          '=512f796d5f5b537500c7e4796d7080f4&chksm'
                          '=8419b4fbb36e3ded08797321c4419bca4b777bf1d11c22cca221cb4bfca0b1b580c70ee64a9a#rd')
        # start_urls = [data["link"] for _input in JsonFileInput('list-res').input_result()]

    def parse(self, response, **kwargs):
        selector = Selector(response)
        soup = BeautifulSoup(selector.get(), 'html.parser')
        items = soup.find_all('div', class_='rich_media_area_extra')
        for item in items:
            item.decompose()
        items = soup.find_all('iframe')
        for item in items:
            item.decompose()
        res = WechatDetailItem()
        res["html"] = str(soup)
        res["timestamp"] = kwargs.get("timestamp")

        return res
