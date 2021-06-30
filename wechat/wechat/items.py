from scrapy import Item, Field


class WechatListItem(Item):
    app_msg_list = Field()


class WechatDetailItem(Item):
    path = Field()
    title = Field()
    category = Field()
    tag = Field()
    summary = Field()
