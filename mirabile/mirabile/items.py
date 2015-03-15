# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class  MirabileItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    author = scrapy.Field()
    title = scrapy.Field()
    related_works = scrapy.Field()
    incipit = scrapy.Field()
    explicit = scrapy.Field()
    references = scrapy.Field()
    shelfmark = scrapy.Field()
    related_projects = scrapy.Field()
    permalink = scrapy.Field()
    html = scrapy.Field()
