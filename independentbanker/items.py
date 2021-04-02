import scrapy


class IndependentbankerItem(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()
    date = scrapy.Field()
