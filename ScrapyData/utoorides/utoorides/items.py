# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class UtooridesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class UtoorideItem(scrapy.Item):
    url = scrapy.Field()
    website = scrapy.Field()
    geonameid = scrapy.Field()
    city = scrapy.Field()
    company = scrapy.Field()
    logo = scrapy.Field()
    country = scrapy.Field()
    services = scrapy.Field()
    price = scrapy.Field()
    appUrl = scrapy.Field()
    bookingViaphone = scrapy.Field()
    seatingCapacity = scrapy.Field()
    luggageCapacity = scrapy.Field()
    typeofvehicle = scrapy.Field()
    typeofcar = scrapy.Field()
    childFriendly = scrapy.Field()
    surgePricing = scrapy.Field()
    wheelChairAssistance = scrapy.Field()
    timestamp = scrapy.Field()
    email = scrapy.Field()
    phone = scrapy.Field()