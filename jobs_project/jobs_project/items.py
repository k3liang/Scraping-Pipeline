# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class JobsProjectItem(scrapy.Item):
    # define the fields for the item here:
    slug = Field()
    language = Field()
    languages = Field()
    req_id = Field()
    title = Field()
    description = Field()
    street_address = Field()
    city = Field()
    state = Field()
    country_code = Field()
    postal_code = Field() 
    location_type = Field()
    latitude = Field()
    longitude = Field()
    tags = Field() 
    tags5 = Field() 
    tags6 = Field() 
    brand = Field()
    promotion_value = Field()
    salary_currency = Field()
    salary_value = Field()
    salary_min_value = Field()
    salary_max_value = Field()
    benefits = Field()
    employment_type = Field()
    hiring_organization = Field()
    source = Field()
    apply_url = Field()
    internal = Field()
    searchable = Field()
    applyable = Field()
    li_easy_applyable = Field()
    ats_code = Field()
    meta_data = Field()
    update_date = Field(serializer=str)
    create_date = Field(serializer=str)
    category = Field()
    full_location = Field()
    short_location = Field()
