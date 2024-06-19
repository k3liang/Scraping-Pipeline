import json
import scrapy

from jobs_project.items import JobsProjectItem
from datetime import datetime

class Jobpider(scrapy.Spider):
    name = 'job_spider'
    custom_settings = {
    	'ITEM_PIPELINES': {
            'jobs_project.pipelines.RedisPipeline': 300,
        	'jobs_project.pipelines.PostgreSQLPipeline': 400,
            'jobs_project.pipelines.MongoDBPipeline': 500,
    	},
	}

    def __init__(self, **kwargs):
        pass

    def start_requests(self):
        json_files = ['/app/data/s01.json','/app/data/s02.json']

        for file in json_files:
            yield scrapy.Request(
                url=f'file://{file}',  
                callback=self.parse_page,
            )

    def parse_page(self, response):
        # load json files using response.text
        # loop over data
        # return items
        data = json.loads(response.text)

        for job_data in data['jobs']:
            job = job_data['data']

            item = JobsProjectItem()
            item['slug'] = job.get('slug', ''),
            item['language'] = job.get('language', ''),
            item['languages'] = job.get('languages', []),
            item['req_id'] = job.get('req_id', ''),
            item['title'] = job.get('title', ''),
            item['description'] = job.get('description', ''),
            item['street_address'] = job.get('street_address', ''),
            item['city'] = job.get('city', ''),
            item['state'] = job.get('state', ''),
            item['country_code'] = job.get('country_code', ''),
            item['postal_code'] = job.get('postal_code', ''), 
            item['location_type'] = job.get('location_type', ''),
            item['latitude'] = job.get('latitude', ''),
            item['longitude'] = job.get('longitude', ''),
            item['tags'] = job.get('tags', []), 
            item['tags5'] = job.get('tags5', []), 
            item['tags6'] = job.get('tags6', []), 
            item['brand'] = job.get('brand', ''),
            item['promotion_value'] = job.get('promotion_value', 0),
            item['salary_currency'] = job.get('salary_currency', ''),
            item['salary_value'] = job.get('salary_value', 0),
            item['salary_min_value'] = job.get('salary_min_value', 0),
            item['salary_max_value'] = job.get('salary_max_value', 0),
            item['benefits'] = job.get('benefits', []),
            item['employment_type'] = job.get('employment_type', ''),
            item['hiring_organization'] = job.get('hiring_organization', ''),
            item['source'] = job.get('source', ''),
            item['apply_url'] = job.get('apply_url', ''),
            item['internal'] = job.get('internal', False),
            item['searchable'] = job.get('searchable', False),
            item['applyable'] = job.get('applyable', False),
            item['li_easy_applyable'] = job.get('li_easy_applyable', False),
            item['ats_code'] = job.get('ats_code', ''),
            item['meta_data'] = json.dumps(job.get('meta_data', '')),
            item['update_date'] = datetime.strptime(job.get('update_date', ''), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S%z'),
            item['create_date'] = datetime.strptime(job.get('create_date', ''), '%Y-%m-%dT%H:%M:%S%z').strftime('%Y-%m-%d %H:%M:%S%z'),
            item['category'] = job.get('category', []),
            item['full_location'] = job.get('full_location', ''),
            item['short_location'] = job.get('short_location', '')

            yield item
