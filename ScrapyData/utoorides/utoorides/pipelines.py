# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html


class UtooridesPipeline(object):
    def process_item(self, item, spider):
        return item
        
from pymongo import MongoClient
class MongoPipeline(object):

	def open_spider(self, spider):
		from utoorides.config import mongoConfiguration
		mongoConfig = mongoConfiguration.get(spider.name)
		client = MongoClient(mongoConfig.get('MONGODB_HOST', 'localhost'), mongoConfig.get('MONGODB_PORT', 27017))
		db = client[mongoConfig.get('MONGODB_DATABASE_NAME')]
		self.col = db[mongoConfig.get('MONGODB_COLLECTION_NAME')]

	def process_item(self, item, spider):
		self.col.insert(dict(item))
