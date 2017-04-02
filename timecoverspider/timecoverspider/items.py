# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

# import scrapy
# 
# 
# class TimecoverspiderItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass



# import the necessary packages
import scrapy
 
class MagazineCover(scrapy.Item):
	image_urls = scrapy.Field()
	session_path = scrapy.Field()
	images = scrapy.Field()
	