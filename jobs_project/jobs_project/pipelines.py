# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import psycopg2
import pymongo
import redis
import json
from datetime import datetime

class PostgreSQLPipeline:
    def open_spider(self, spider):
        self.conn = psycopg2.connect(
            dbname='scrapydb',
            user='scrapyuser',
            password='scrapypassword',
            host='postgres'
        )
        self.cur = self.conn.cursor()
        self.cur.execute('''
            CREATE TABLE IF NOT EXISTS raw_table (
                id                      serial PRIMARY KEY,
                slug                    text,
                language                text,
                languages               text[],
                req_id                  text,
                title                   text,
                description             text,
                street_address          text,
                city                    text,
                state                   text,
                country_code            text,
                postal_code             text,
                location_type           text,
                latitude                numeric,
                longitude               numeric,
                tags                    text[],
                tags5                   text[],
                tags6                   text[],
                brand                   text,
                promotion_value         numeric,
                salary_currency         text,
                salary_value            numeric,
                salary_min_value        numeric,
                salary_max_value        numeric,
                benefits                text[],
                employment_type         text,
                hiring_organization     text,
                source                  text,
                apply_url               text,
                internal                boolean,
                searchable              boolean,
                applyable               boolean,
                li_easy_applyable       boolean,
                ats_code                text,
                meta_data               text,
                update_date             timestamp with time zone,
                create_date             timestamp with time zone,
                category                text[],
                full_location           text,
                short_location          text
            )
        ''')
        self.conn.commit()

    def close_spider(self, spider):
        self.cur.close()
        self.conn.close()

    def process_item(self, item, spider):
        if not item:
            return None
        
        self.cur.execute('''
            INSERT INTO raw_table (slug,language,languages,req_id,title,description,street_address,city,state,country_code,postal_code,location_type,latitude,longitude,tags,tags5,tags6,brand,promotion_value,salary_currency,salary_value,salary_min_value,salary_max_value,benefits,employment_type,hiring_organization,source,apply_url,internal,searchable,applyable,li_easy_applyable,ats_code,meta_data,update_date,create_date,category,full_location,short_location) VALUES (%s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s,%s, %s, %s, %s, %s)
        ''', (item['slug'],item['language'],item['languages'],item['req_id'],item['title'],item['description'],item['street_address'],item['city'],item['state'],item['country_code'],item['postal_code'],item['location_type'],item['latitude'],item['longitude'],item['tags'],item['tags5'],item['tags6'],item['brand'],item['promotion_value'],item['salary_currency'],item['salary_value'],item['salary_min_value'],item['salary_max_value'],item['benefits'],item['employment_type'],item['hiring_organization'],item['source'],item['apply_url'],item['internal'],item['searchable'],item['applyable'],item['li_easy_applyable'],item['ats_code'],item['meta_data'],item['update_date'],item['create_date'],item['category'],item['full_location'],item['short_location']))

        self.conn.commit()
        return item

class MongoDBPipeline:
    def open_spider(self, spider):
        self.client = pymongo.MongoClient('mongodb://root:example@mongodb:27017/')
        self.db = self.client['scrapydb']
        self.collection = self.db['raw_collection']

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if not item:
            return None

        self.collection.insert_one(dict(item))
        return item

class RedisPipeline:
    def open_spider(self, spider):
        self.r = redis.Redis(host='redis', port=6379)

    def close_spider(self, spider):
        self.r.close()

    def process_item(self, item, spider):
        item_json = json.dumps(dict(item))

        if not self.r.sismember('scrapy_items', item_json):
            self.r.sadd('scrapy_items', item_json)
            return item
        return None