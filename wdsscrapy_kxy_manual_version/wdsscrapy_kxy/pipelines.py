# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs
import os

JSON_PATH = os.getcwd().replace('\\', '/') + '/wds_kxy.json'

class WdsscrapyKxyPipeline(object):
	def __init__(self):
		self.file = codecs.open(JSON_PATH, 'wb', encoding='utf-8')

	def process_item(self, item, spider):
		line = json.dumps(dict(item), ensure_ascii=False)
		#self.file.write('[')
		self.file.write(line)
		#self.file.write(']')
		return item

	def spider_closed(self, spider):
		self.file.close()