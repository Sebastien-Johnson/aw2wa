# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class PdfItem(scrapy.Item):
    file_urls = scrapy.Field()
    files = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    source_url = scrapy.Field()
    pdf_url = scrapy.Field()
    extracted_text = scrapy.Field()
    page_count = scrapy.Field()
    file_size = scrapy.Field()
