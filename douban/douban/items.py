# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DoubanItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name=scrapy.Field()
    description=scrapy.Field()
    url=scrapy.Field()

class CsdnItem(scrapy.Item):
	title=scrapy.Field()
	description=scrapy.Field()
	url=scrapy.Field()
	viewpoint=scrapy.Field()
class ZhihuItem(scrapy.Item):
	url=scrapy.Field()
	answer=scrapy.Field()
	description=scrapy.Field()
	title=scrapy.Field()
	name=scrapy.Field()

class CnBlogItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    description=scrapy.Field()
    url=scrapy.Field()
class ZhihuAnswerItem(scrapy.Item):
	url=scrapy.Field()
	answer=scrapy.Field()
	question=scrapy.Field()
	name=scrapy.Field()