# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Professors(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pid = scrapy.Field()
    name = scrapy.Field()
    title = scrapy.Field()
    department = scrapy.Field()
    email = scrapy.Field()

class Teach(scrapy.Item):
    professor_id = scrapy.Field()
    course_id = scrapy.Field()
    
class Course(scrapy.Item):
    cid = scrapy.Field()
    cname = scrapy.Field()
    lang = scrapy.Field()
    credit = scrapy.Field()
    etype = scrapy.Field()