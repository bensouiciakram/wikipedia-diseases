# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DiseasesItem(scrapy.Item):
    date = scrapy.Field()
    death = scrapy.Field()
    death_toll = scrapy.Field()
    confirmed_cases = scrapy.Field()
    disease = scrapy.Field()
    url = scrapy.Field()