# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class RaceDataItem(scrapy.Item):
    source_url = scrapy.Field()
    pdf_url = scrapy.Field()
    file_path = scrapy.Field()
    tables = scrapy.Field()
    region = scrapy.Field()
    year = scrapy.Field()
    track_event = scrapy.Field()