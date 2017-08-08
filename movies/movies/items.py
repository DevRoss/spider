# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MoviesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    name = scrapy.Field()
    director = scrapy.Field()
    screenwriter = scrapy.Field()
    starrings = scrapy.Field()
    categories = scrapy.Field()
    country_or_region = scrapy.Field()
    languages = scrapy.Field()
    release_date = scrapy.Field()
    runtime = scrapy.Field()
    other_names = scrapy.Field()
    rate = scrapy.Field()
    id = scrapy.Field()


class MoviesNetItem(scrapy.Item):
    has_relation = scrapy.Field()


class MoviesCategoriesItem(scrapy.Item):
    category_and_movies = scrapy.Field()


class MoviesStarringItem(scrapy.Item):
    starring_and_movies = scrapy.Field()
