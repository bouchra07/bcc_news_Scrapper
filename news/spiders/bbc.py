# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from readability import Document
import datetime
from pprint import pprint

class Articles(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    published = scrapy.Field()
    body = scrapy.Field()
    tag_text = scrapy.Field()
    month = scrapy.Field()

class BbcSpider(CrawlSpider):
    
    name = 'bbc'
    allowed_domains = ['bbc.com']
    start_urls = ['http://bbc.com/news']

    rules = (
        Rule(LinkExtractor(), callback='parse_item', follow=True),
    )

    def reconcile_url_base(self, raw_urls):
        start_urls2 = ['http://www.bbc.com/']
        base_added_urls = [(start_urls2[0] + x) if x[:4]!='http' else x for x in raw_urls ]

        return base_added_urls

    def parse_item(self, res):        
        title = self.get_title(res)
        article = Articles()  
        substring = "coronavirus"      
        # Only do further processing if there is a title element in the page
        if ((title != None) and (substring in self.get_body(res)) and (self.get_year(res) == 2020) and ( (self.get_tagtext(res) == "Health") or (self.get_tagtext(res) == "World") or (self.get_tagtext(res) == "Business") or (self.get_tagtext(res) == "Technology")or (self.get_tagtext(res) == "Science & Environment")or (self.get_tagtext(res) == "Entertainment & Arts")or (self.get_tagtext(res) == "Politics") ))  :
            article = Articles()
            article['url'] = res.url 
            article['title']=title
            article['body']= self.get_body(res)
            article['published']= self.get_published(res)
            article['tag_text']= self.get_tagtext(res)
            article['month']= self.get_month(res)
            # self.log(article)           
            return article
        else:
            return None

    def get_title(self, res):
        """
        Get the title of the article
        """
        title = res.css('h1.story-body__h1 ::text').extract_first()
        return title

    def get_body(self, res):
        """
        Get the actual text of the article
        """
        raw = res.css('div.story-body__inner p ::text')
        body =  ''.join(raw.extract())
        return body

    def get_year(self, res):
        """
        Get the article timestamp
        """
        timestamp = res.css('div.story-body div.date ::attr(data-seconds)').extract_first()     
        year = datetime.datetime.fromtimestamp(int(timestamp)).year
        return year
    
    def get_month(self, res):
        """
        Get the article timestamp
        """
        timestamp = res.css('div.story-body div.date ::attr(data-seconds)').extract_first()     
        monthinteger = datetime.datetime.fromtimestamp(int(timestamp)).month
        month = datetime.date(1900, monthinteger, 1).strftime('%B')

        return month
        
    
    def get_published(self, res):
        """
        Get the article timestamp
        """
        #timestamp = res.css('div.story-body div.date ::attr(data-seconds)').extract_first()     
        #published = datetime.datetime.fromtimestamp(int(timestamp))
        published =res.xpath('//div[@class="story-body"]//ul[@class="mini-info-list"]//div/text()').extract_first()
        return published


    def get_tagtext(self, res):
        """
        Get the actual text of the article
        """
        tag_text = res.xpath('//div[contains(@class,"secondary-navigation")]//a[contains(@class,"secondary-navigation__title")]/span/text()').extract_first()
        if tag_text is None:
            tag_text = res.xpath("//div[@class='container-width-only']//span[@class='index-title__container']//a/text()").extract_first()
                #two ways to get type
        return tag_text

    
