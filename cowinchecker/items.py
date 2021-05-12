# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

from scrapy.item import Field, Item


class AvailableLocation(Item):
    # define the fields for your item here like:
    state_name = Field()
    district_name = Field()
    center_id = Field()
    center_name = Field()
    pincode = Field()
    date = Field()
    available_capacity = Field()
    min_age_limit = Field()
    fee_type = Field()
    vaccine = Field()
    slots = Field()
