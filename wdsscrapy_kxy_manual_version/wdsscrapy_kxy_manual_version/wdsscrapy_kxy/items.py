# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class WdsscrapyKxyItem(scrapy.Item):
    # type of attributes is scrapy.Field
    total_amount = scrapy.Field() # current total amount
    total_people_number = scrapy.Field() # number of current sposors
    remaining_time = scrapy.Field() # the remaining time
    current_sponsors = scrapy.Field() # the first page of sponsors' name
    current_sponsors_amount = scrapy.Field() # the corresponding amount to the sponsors in first page
