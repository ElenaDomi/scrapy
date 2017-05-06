# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class SpidersItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class ShuichanItem(Item):
    phone = Field()
    mobile = Field()
    publisher = Field()
    contacts = Field()
    address = Field()
    price = Field()
    email = Field()
    publish = Field()
    expired = Field()
    website = Field()
    content = Field()
    views = Field()
    id = Field()
    unknown = Field()
    pass