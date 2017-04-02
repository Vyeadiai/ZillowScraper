# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import scrapy
import os
import os.path
from scrapy.contrib.pipeline.images import ImagesPipeline
from timecoverspider.settings import IMAGES_STORE


class SessionImagesPipeline(ImagesPipeline):

	def get_media_requests(self, item, info):
		for image_url in item['image_urls']:
			yield scrapy.Request(image_url)

	def item_completed(self, results, item, info):		
		# iterate over the local file paths of all downloaded images
		for result in [x for ok, x in results if ok]:
			path = result['path']
			# here we create the session-path where the files should be in the end
			# you'll have to change this path creation depending on your needs
			target_path = os.path.join(item['session_path'], os.path.basename(path))
			
			
			sourceFile = IMAGES_STORE + "/" + path
			
			# try to move the file and raise exception if not possible, else it was successful
			if os.rename(sourceFile, target_path):
				raise ImageException("Could not move image to target folder")
			
			
			# here we'll write out the result with the new path,
			# if there is a result field on the item (just like the original code does)
			if self.IMAGES_RESULT_FIELD in item.fields:
				result['path'] = target_path
				
		return item
		