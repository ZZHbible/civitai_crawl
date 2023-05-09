# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class CreatorItem(scrapy.Item):
    # define the fields for your item here like:
    name = scrapy.Field()
    model_num=scrapy.Field()
    link=scrapy.Field()

class ModelItem(scrapy.Item):
    id=scrapy.Field()
    type=scrapy.Field()
    downloadCount=scrapy.Field()
    ratingCount=scrapy.Field()
    rating=scrapy.Field()
    base_model=scrapy.Field()
    images_link=scrapy.Field()
    images_prompt=scrapy.Field()
    download_link=scrapy.Field()

