# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst, Join
from w3lib.html import remove_tags

def remove_line(value):
    return value.replace('\n', '').strip()


class AmazonBookItem(scrapy.Item):
    # define the fields for your item here like:
    Title = scrapy.Field()
    Author = scrapy.Field(
        input_processor= MapCompose(str.strip, remove_tags, remove_line),
        output_processor= TakeFirst()
    )
    Price = scrapy.Field()
    Image_Link = scrapy.Field()
    #pass
