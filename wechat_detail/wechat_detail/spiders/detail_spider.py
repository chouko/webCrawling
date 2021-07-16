from urllib.parse import urlparse

from bs4 import BeautifulSoup
from scrapy import Spider, Selector, Request

from common.file_input import JsonFileInput
from wechat_detail.items import WechatDetailItem


class WechatDetailSpider(Spider):
    name = 'wechat_detail'

    def start_requests(self):
        # i = 0
        # _input = JsonFileInput('list-res').input_result()[:20]
        # for data in _input:
        #     yield Request(data["link"], callback=self.parse,
        #                   cb_kwargs=dict(timestamp=data["create_time"], title=data["title"]))
        #     time.sleep(3)
        #     i += 1
        yield Request('http://mp.weixin.qq.com/s?__biz=MzA4NDg0NzYyMg==&mid=2651711890&idx=1&sn'
                      '=512f796d5f5b537500c7e4796d7080f4&chksm'
                      '=8419b4fbb36e3ded08797321c4419bca4b777bf1d11c22cca221cb4bfca0b1b580c70ee64a9a#rd',
                      callback=self.parse, headers={"Referer": "https://v.qq.com/",
                                                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                                  "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                                  "Chrome/91.0.4472.124 Safari/537.36 "},
                      cb_kwargs=dict(timestamp=1625100159, title="加拿大公民身份的好处是什么？ 从永久居民到加拿大公民的七大理由！"))

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
        res["html"], res["image_urls"] = self.change_src_path(soup)
        res["timestamp"] = kwargs.get("timestamp")
        res["title"] = kwargs.get("title")
        res["summary"] = ""
        res["category"] = "NEWS"

        return res

    def change_src_path(self, soup):
        imgs = soup.find_all("img")
        original_urls = []
        for img in imgs:
            if "data-src" in img.attrs:
                original_url = img.attrs["data-src"]
                del img.attrs["data-src"]

            elif "src" in img.attrs:
                original_url = img.attrs["src"]
            else:
                original_url = ""
            if original_url.startswith("//"):
                original_url = "https:" + original_url
            img.attrs["src"] = '/webCrawling'+urlparse(original_url).path
            if "data-type" in img.attrs:
                img.attrs["src"] += '.' + img.attrs["data-type"]
            original_urls.append(original_url) if original_url != "" else None
        return str(soup), original_urls
