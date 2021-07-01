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
        self.__index = 325

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
        if len(result['app_msg_list']) == 0:
            raise CloseSpider("已经没有新闻了：" + res)
        if result['base_resp']['ret'] == 200013:
            print("频繁了, 开始sleep………………")
            time.sleep(7200)
            print("试着重新开爬………………")
            self.__index -= 5
        item = items.WechatListItem()
        item["app_msg_list"] = result['app_msg_list']
        return item
