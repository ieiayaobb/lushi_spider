# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PlayerItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()


class MatchItem(scrapy.Item):
    match_name = scrapy.Field()
    left_player = scrapy.Field()
    left_player_id = scrapy.Field()
    right_player = scrapy.Field()
    right_player_id = scrapy.Field()


class CompeteItem(scrapy.Item):
    match_name = scrapy.Field()
    left_job = scrapy.Field()
    right_job = scrapy.Field()
    winner = scrapy.Field()