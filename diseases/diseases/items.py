# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst



class DiseasesItem(scrapy.Item):
    date = scrapy.Field(output_processor=TakeFirst())
    death = scrapy.Field(output_processor=TakeFirst())
    death_toll = scrapy.Field(output_processor=TakeFirst())
    confirmed_cases = scrapy.Field(output_processor=TakeFirst())
    disease = scrapy.Field(output_processor=TakeFirst())
    url = scrapy.Field(output_processor=TakeFirst())