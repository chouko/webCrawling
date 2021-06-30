import json
import time
from random import randint

from scrapy import Spider, Request, Selector
from scrapy.exceptions import CloseSpider

from setting import WHCHAT_LIST_FORMAT
from articlelist import listsearch
from wechat import items


class ListSpider(Spider):
    name = 'wechat_list'
    allowed_domains = ['mp.weixin.qq.com/']

    def __init__(self, name=None, **kwargs):
        super().__init__(name, **kwargs)
        self.__search = listsearch.ListSearch()
        self.__index = 295

    def start_requests(self):
        while True:
            yield Request(WHCHAT_LIST_FORMAT.format(self.__index, self.__search.params["token"][0]))
            time.sleep(randint(3, 5))
            self.__index += 5

    def parse(self, response, **kwargs):
        res = Selector(response).xpath("//pre/text()").get()
        try:
            result = json.loads(res)
        except BaseException:
            raise CloseSpider("异常发生：" + res)

        item = items.WechatListItem()
        item["app_msg_list"] = result['app_msg_list']
        return item
