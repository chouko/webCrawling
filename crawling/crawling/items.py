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
    resource_links = Field()


class JsonOutputsSingleItem(Item):
    path = Field()
    title = Field()
    category = Field()
    tag = Field()
    summary = Field()
