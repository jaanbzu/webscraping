# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class RightmoveItem(scrapy.Item):
    # define the fields for your item here like:
    address = scrapy.Field()
    price = scrapy.Field()
    name = scrapy.Field()
    phone = scrapy.Field()

