# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from readability import Document

class NewsPipeline(object):
    def process_item(self, item, spider):
        return item


class MongoPipeline(object):    
    collection_name = 'bbc_articles'

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
    
    @classmethod
    def from_crawler(cls, crawler):
        return cls(mongo_uri = crawler.settings.get('MONGO_URI'), mongo_db = crawler.settings.get('MONGO_DATABASE', 'news'))

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()
        

    def process_item(self, item, spider):
        self.db[self.collection_name].insert_one(dict(item))
        return item

    
    class SanitizerPipeline(object):
        """
        Sanitize document using Readability but this is not implemented fully 
        and not added to the pipeline because it simply suck. Keeps failing to 
        extract important elements and would still require the use of hand tuned spider selector
        for certain fields. We stick to using "surgically precise" hand crafted extraction selectors 
        which produce way cleaner and usable outpus.
        """
        def process_item(self, item, spider):
            # item["body"] = Document(item["body"])
            return item

