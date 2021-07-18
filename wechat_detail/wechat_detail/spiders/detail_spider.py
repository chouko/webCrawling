import time
from urllib.parse import urlparse

from bs4 import BeautifulSoup
from scrapy import Spider, Selector, Request

from wechat_detail.items import WechatDetailItem

from common.file_input import JsonFileInput


class WechatDetailSpider(Spider):
    name = 'wechat_detail'

    def start_requests(self):
        i = 0
        _input = JsonFileInput('list-res').input_result()[:20]
        for data in _input:
            yield Request(data["link"], callback=self.parse,
                          headers={"Referer": "https://v.qq.com/",
                                   "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                                                 "AppleWebKit/537.36 (KHTML, like Gecko) "
                                                 "Chrome/91.0.4472.124 Safari/537.36 "},
                          cb_kwargs=dict(timestamp=data["create_time"], title=data["title"]))
            time.sleep(3)
            i += 1

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
        res["html"], res["image_urls"] = self.change_src_path(soup, kwargs.get("timestamp"))
        res["timestamp"] = kwargs.get("timestamp")
        res["title"] = kwargs.get("title")
        res["summary"] = ""
        res["category"] = "NEWS"

        return res

    def change_src_path(self, soup, dir_name):
        original_urls = []
        # qr_code = soup.find("div", class_='qr_code_pc_inner')
        # del qr_code
        for img in soup.find_all("img"):
            if "data-src" in img.attrs:
                original_url = img.attrs["data-src"]
                del img.attrs["data-src"]

            elif "src" in img.attrs:
                original_url = img.attrs["src"]
            else:
                original_url = ""
            if original_url.startswith("//"):
                original_url = "https:" + original_url
            img.attrs["src"] = '/webCrawling' + urlparse(original_url).path
            if "data-type" in img.attrs:
                img.attrs["src"] += '.' + img.attrs["data-type"]
            original_urls.append(original_url) if original_url != "" else None
        return str(soup), original_urls
