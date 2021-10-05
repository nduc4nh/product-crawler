# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
# used for assertion
from scrapy.exceptions import DropItem
import pymongo
from kafka import KafkaProducer
import json

class MongoShopeePipeline:
    collection = "items"

    def __init__(self, mongo_uri, mongodb):
        self.mongo_uri = mongo_uri
        self.mongodb = mongodb

    # This classmethod create an instance of the pipeline everytime it is used
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("MONGO_URI"),
            mongodb=crawler.settings.get("MONGO_DATABASE")
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongodb]

    def process_item(self, item, spider):
        if is_item(item):
            item_adapter = ItemAdapter(item)
            name = item_adapter.get('name')
            self.db[self.collection].replace_one(
                {'name': name}, item_adapter.asdict(), upsert=True)
            return item
        raise DropItem("Unsupported Item!")

    def close_spider(self, spider):
        self.client.close()


class CloudantShopeePipeline:
    topic  = "movie"
    def __init__(self, brokers):
        self.brokers = brokers

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get("BROKERS"),
        )

    def open_spider(self, spider):
        self.producer = KafkaProducer(security_protocol="SASL_SSL", bootstrap_servers=self.brokers, sasl_mechanism="PLAIN", sasl_plain_username="token",
                                 sasl_plain_password="0wg8-0XRfuKR8OChD31WlZQ78cPT753C8N_fQTvsOu8P", value_serializer=lambda x: json.loads(x.decode('utf-8')), request_timeout_ms=10000)
    
    def process_item(self, item, spider):
        if is_item(item):
            item_adapter = ItemAdapter(item)
            self.producer.get(self.topic, value = item_adapter.asdict())
            return item
        raise DropItem("Unsupported Item!")
    
    def close_spider(self, spider):
        self.producer.close()
