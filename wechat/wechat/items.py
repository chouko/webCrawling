from scrapy import Item, Field


class WechatListItem(Item):
    app_msg_list = Field()

