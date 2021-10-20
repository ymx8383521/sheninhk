# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class SheninhkItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    detail_url=scrapy.Field()
    load_path=scrapy.Field()
    image_urls = scrapy.Field()
    images = scrapy.Field()
    image_paths = scrapy.Field()
