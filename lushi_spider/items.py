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
    player_left = scrapy.Field()
    player_right = scrapy.Field()


class CompeteItem(scrapy.Item):
    job_left = scrapy.Field()
    job_right = scrapy.Field()
    winner = scrapy.Field()