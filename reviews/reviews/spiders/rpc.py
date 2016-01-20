# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector
from reviews.items import EventItem
from reviews.pipelines import MongoDBPipeline
from selenium import webdriver
from time import sleep
import string
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class RcpLondon(Spider):
    name = "rcpspidy"
    allowed_domains = ["rcplondon.ac.uk"]
    start_urls = ['https://www.rcplondon.ac.uk/events']
    db = MongoDBPipeline()

    def __init__(self):
        self.driver = webdriver.Firefox()
 

    def parse(self, response):

        self.driver.get(response.url)
        load_more_btn = self.driver.find_element_by_xpath('//*[@id="search-listing"]/div[2]/div/div[4]/ul/li/a')
        while True:
            source = self.driver.page_source
            source = source.encode('ascii', 'ignore')
            event_source = Selector(text=source)
            events_list = event_source.xpath('//*[@id="search-listing"]/div[2]/div/div[4]/div[@class="view-content"]/ul/li/div/span/div')
            load_more_text = event_source.xpath('translate(normalize-space(//*[@id="search-listing"]/div[2]/div/div[4]/ul/li/a/text()), " ", " ")').extract()[0]

            try: 
                if load_more_text == 'Load more':
                   load_more_el = self.driver.find_element_by_xpath('//*[@id="search-listing"]/div[2]/div/div[4]/ul/li/a')
                   load_more_el.click()
                   sleep(3)
                else:
                    print len(events_list)
                    #map(self.parse_event, events_list)
                    for event in events_list:
                        url = ['http://'] + self.allowed_domains + event.xpath('div[@class="caption"]/div/h3/a/@href').extract()
                        url = string.join(url, '')

                        if self.db.collection.find_one({'url': url}):
                            fetched_event = self.db.collection.find_one({'url': url})
                            print fetched_event
                            parsed_event = {}
                            parsed_event['title'] = event.xpath('div[@class="caption"]/div/h3/a/text()').extract()
                            parsed_event['url'] = url
                            parsed_event['description'] = event.xpath('div[@class="caption"]/div/p/text()').extract()
                            parsed_event['datetime_range'] =  event.xpath('div[@class="caption-footer"]/div[contains(@class, "field-name-field-datetime-range")]/span/text()').extract()
                            parsed_event['event_venue'] = event.xpath('div[@class="caption-footer"]/div[contains(@class, "field-name-field-event-venue")]/text()').extract()
                            parsed_event['cpd_credits'] = event.xpath('div[@class="caption-footer"]/div[contains(@class, "field-name-field-cpd-credits")]/text()[2]').extract()

                            self.db.collection.update({'url': url}, {"$set": parsed_event})
                            print fetched_event 

                        else:

                            parsed_event = EventItem()
                            parsed_event['title'] = event.xpath('div[@class="caption"]/div/h3/a/text()').extract()
                            parsed_event['url'] = url
                            parsed_event['description'] = event.xpath('div[@class="caption"]/div/p/text()').extract()
                            parsed_event['datetime_range'] =  event.xpath('div[@class="caption-footer"]/div[contains(@class, "field-name-field-datetime-range")]/span/text()').extract()
                            parsed_event['event_venue'] = event.xpath('div[@class="caption-footer"]/div[contains(@class, "field-name-field-event-venue")]/text()').extract()
                            parsed_event['cpd_credits'] = event.xpath('div[@class="caption-footer"]/div[contains(@class, "field-name-field-cpd-credits")]/text()[2]').extract()
                            yield parsed_event

                    self.driver.close()
                    break
            except Exception as e:
                print e
                break