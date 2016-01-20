# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html
from scrapy.item import Item, Field

class EventItem(Item):

    title = Field()
    url = Field()
    datetime_range = Field()
    cpd_credits = Field()
    event_venue = Field()
    description = Field()