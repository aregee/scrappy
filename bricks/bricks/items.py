# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field


class MedMeetingsList(Item):
    title = Field()
    url = Field()
    next_date = Field()
    provider = Field()
    course_duration = Field()
    course_type = Field()
    course_description = Field()
