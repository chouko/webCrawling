from scrapy import Item, Field


class WechatListItem(Item):
    app_msg_list = Field()


class WechatDetailItem(Item):
    html = Field()
    timestamp = Field()
