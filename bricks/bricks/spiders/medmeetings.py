from scrapy import Spider
from scrapy.selector import Selector
from bricks.items import MedMeetingsList
from bricks.pipelines import MongoDBPipeline
from scrapy.selector import HtmlXPathSelector
from selenium import webdriver
from time import sleep
import selenium
import string
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class MedMeetings(Spider):
    name = "medmeetings"
    allowed_domains = ["medmeetings.co.uk"]
    start_urls = ["http://www.medmeetings.co.uk/all/all"]
    db = MongoDBPipeline()

    def parse(self, response):
        courses = Selector(response).xpath('//*[@id="courses"]/div[@class="course-listing"]')
        for course in courses:

            course_url = ['http://'] + self.allowed_domains + course.xpath('div[@class="course_listing_title"]/h3/a/@href').extract()
            course_url = string.join(course_url, '')

            if self.db.collection.find_one({'url': course_url}):
                item = {}
                item['title'] = course.xpath(
                'div[@class="course_listing_title"]/h3/a/span[@class="course_name_main"]/text()').extract()
                course_url = ['http://'] + self.allowed_domains + course.xpath('div[@class="course_listing_title"]/h3/a/@href').extract()
                item['url'] = string.join(course_url, '')
                course_elearn = course.xpath('div[@class="course-block-details"]/span[@class="elearning"]/text()').extract()
                course_offline = course.xpath('div[@class="course-block-details"]/span[@class="course"]/text()').extract()
                next_date = course.xpath('div[@class="course-block-details"]/b[contains(text(),"Next Date:")][normalize-space()="Next Date:"]').extract()
                if next_date: 
                    next_date_val = course.xpath('translate(normalize-space(div[@class="course-block-details"]/text() [4])," ", " ")').extract()
                    item['next_date'] = next_date_val
                    item['provider'] = course.xpath('translate(normalize-space(div[@class="course-block-details"]/text() [6])," ", "")').extract()
                else:
                    item['provider'] = course.xpath('translate(normalize-space(div[@class="course-block-details"]/text() [4])," ", "")').extract()
                item['course_description'] = course.xpath('p/text()').extract()
                item['course_duration'] = course_elearn if course_elearn else course_offline
                item['course_type'] = 'online' if course_elearn else 'course_offline'
                
                self.db.collection.update({'url': course_url}, {'$set': item})
            else:

                item = MedMeetingsList()
                item['title'] = course.xpath(
                    'div[@class="course_listing_title"]/h3/a/span[@class="course_name_main"]/text()').extract()
                course_url = ['http://'] + self.allowed_domains + course.xpath('div[@class="course_listing_title"]/h3/a/@href').extract()
                item['url'] = string.join(course_url, '')
                course_elearn = course.xpath('div[@class="course-block-details"]/span[@class="elearning"]/text()').extract()
                course_offline = course.xpath('div[@class="course-block-details"]/span[@class="course"]/text()').extract()
                next_date = course.xpath('div[@class="course-block-details"]/b[contains(text(),"Next Date:")][normalize-space()="Next Date:"]').extract()
                if next_date: 
                    next_date_val = course.xpath('translate(normalize-space(div[@class="course-block-details"]/text() [4])," ", " ")').extract()
                    item['next_date'] = next_date_val
                    item['provider'] = course.xpath('translate(normalize-space(div[@class="course-block-details"]/text() [6])," ", "")').extract()
                else:
                    item['provider'] = course.xpath('translate(normalize-space(div[@class="course-block-details"]/text() [4])," ", "")').extract()
                item['course_description'] = course.xpath('p/text()').extract()
                item['course_duration'] = course_elearn if course_elearn else course_offline
                item['course_type'] = 'online' if course_elearn else 'course_offline'
                yield item