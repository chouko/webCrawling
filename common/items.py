from scrapy import Item, Field


class JsonOutputsSingleItem(Item):
    path = Field()
    title = Field()
    category = Field()
    tag = Field()
    summary = Field()
