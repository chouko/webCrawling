from bs4 import BeautifulSoup
from scrapy import Spider, Selector

from common.file_input import JsonFileInput


class WechatDetailSpider(Spider):
    name = 'wechat_detail'
    start_urls = JsonFileInput('list-res').input_result()

    def parse(self, response, **kwargs):
        selector = Selector(response)
        article_content = selector.xpath("//div/[@class='rich_media_inner']")
        to_be_deleted = article_content.xpath(".//div/[@class='rich_media_area_extra']").get()
        print(article_content.get())
        soup = BeautifulSoup(to_be_deleted.get(), 'lxml')
        print(soup.string)
        print(to_be_deleted)
        pass
