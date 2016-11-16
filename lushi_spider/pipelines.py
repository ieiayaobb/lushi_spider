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
        self.race_collection = db['race']
        self.race_collection.ensure_index('race_name')
        self.match_collection = db['match']
        self.match_collection.ensure_index('match_name')
        self.compete_collection = db['compete']
        self.compete_collection.ensure_index('match_id')
        self.player_collection = db['player']
        self.player_collection.ensure_index('player_name')

    def process_item(self, item, spider):
        mongo_item = dict(item)
        if isinstance(item, MatchItem):
            # handle player
            left_player = item['left_player']
            right_player = item['right_player']
            if self.player_collection.count({'player_name': left_player}) == 0:
                self.player_collection.insert({
                    'player_name': left_player
                })
            left_player_id = self.player_collection.find_one({'player_name': left_player})['_id']
            mongo_item['left_player_id'] = left_player_id

            if self.player_collection.count({'player_name': right_player}) == 0:
                self.player_collection.insert({
                    'player_name': right_player
                })
            right_player_id = self.player_collection.find_one({'player_name': right_player})['_id']
            mongo_item['right_player_id'] = right_player_id

            # handle race
            race_name = mongo_item['race_name']
            if self.race_collection.count({'race_name': race_name}) == 0:
                self.race_collection.insert({
                    'race_name': race_name
                })
            race_id = self.race_collection.find_one({'race_name': race_name})['_id']
            mongo_item['race_id'] = race_id

            self.match_collection.insert(mongo_item)

        if isinstance(item, CompeteItem):
            match_name = item['match_name'].decode('utf8')
            mongo_item['match_id'] = self.match_collection.find_one({'match_name': match_name})['_id']
            self.compete_collection.insert(mongo_item)
        return item
