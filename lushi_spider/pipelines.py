# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo.mongo_client import MongoClient

from lushi_spider.items import MatchItem, CompeteItem
from lushi_spider.settings import MONGODB_IP


class LushiSpiderPipeline(object):
    def __init__(self):
        mongodb_uri = 'mongodb://' + MONGODB_IP + ':27017/'
        connection = MongoClient(mongodb_uri)
        db = connection['lushi']
        self.match_collection = db['match']
        self.compete_collection = db['compete']

    def process_item(self, item, spider):
        mongo_item = dict(item)
        if isinstance(item, MatchItem):
            self.match_collection.insert(mongo_item)
        if isinstance(item, CompeteItem):
            self.compete_collection.insert(mongo_item)
        return item
