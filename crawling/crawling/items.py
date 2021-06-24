# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class CrawlingItem(Item):
    # define the fields for your item here like:
    source_url = Field()
    title = Field()
    localtime = Field()
    body = Field()
    images = Field()
    image_urls = Field()
    category = Field()
    summary = Field()


class JsonOutputItem1(Item):
    resourceList = Field()


class JsonOutputItem2(Item):
    fileRes = Field()


class JsonOutputItem3(Item):
    path = Field()
    title = Field()
    category = Field()
    tag = Field()
    summary = Field()
