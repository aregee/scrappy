# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class BricksItem(Item):
    title = Field()
    url = Field()
    review_body = Field()
    locality = Field()

class BrickReviewItem(Item):
    title = Field()
    url = Field()
    average_rate = Field()
    locality = Field()
    projects_available = Field()
    recomended_for = Field()
    properties_available = Field()
    ratings = Field()
    review_body = Field()
    meta_data = Field()
