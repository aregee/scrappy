# -*- coding: utf-8 -*-
from scrapy import Spider
from scrapy.selector import Selector
from reviews.items import ReviewsItem
from reviews.pipelines import MongoDBPipeline
from selenium import webdriver
from time import sleep
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

mdb = MongoDBPipeline(collection_name='overviews')
get_all = mdb.get_all()

class ReviewerSpider(Spider):
    name = "reviewer"
    allowed_domains = ["magicbricks.com"]
    URLS = [str(x['meta_data']['review']['review_url']) for x in mdb.get_all() if x['meta_data']['review']['review_url']]
    start_urls =URLS
    #['http://www.magicbricks.com/real-estate-property-reviews/Vaishali-in-Ghaziabad#reviewResult'] #URLS[:3]


    def __init__(self):
        dcap = dict(DesiredCapabilities.PHANTOMJS)
        dcap["phantomjs.page.settings.userAgent"] = (
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36;"
        )
        #self.driver = webdriver.PhantomJS(
        #    executable_path='/usr/local/bin/phantomjs', desired_capabilities=dcap)
        self.driver = webdriver.Firefox()
    def parse(self, response):
        self.driver.get(response.url)
        self.pagers = []
        self.val = 1
        while True:
            source = self.driver.page_source
            sou2 = source.encode('ascii', 'ignore')
            reviewObj = Selector(text=sou2)
            reviewSearchList = reviewObj.xpath('//div[@id="reviewResult"]/div/div[@class="reviewsSearchList"]/ul/li')
            paginated = reviewObj.xpath('//div[@id="pagination"]/a[@class="act"]').extract()
            print (paginated)
            litVal = len(paginated)
            try:
                if litVal > 1:
                    nextEl = self.driver.find_element_by_xpath('//*[@id="pagination"]/a[%s]'% self.val)
                for review in reviewSearchList:
                #print review.extract()
                    item = ReviewsItem()
                    reviewTitle = review.xpath('div[@class="detailCont"]/h5/text()').extract()
                    item['url']  = response.url
                    if reviewTitle:
                        item['title'] = reviewTitle[0] or reviewTitle
                    reviewBody = review.xpath('div[@class="detailCont"]/div[3]/div/span[2]/text()').extract()
                    if reviewBody:
                        item['review_body'] = reviewBody[0] or reviewBody
                    reviewBrief = review.xpath('div[@class="detailCont"]/div[3]/div/text()').extract()
                    if reviewBrief:
                        item['meta_data'] = dict(data=reviewBrief[0] or reviewBrief)
                    reviewAuthor = review.xpath('div[@class="imageCont"]/a[2]/text()').extract()
                    if reviewAuthor:
                        item['author'] = reviewAuthor[0] or reviewAuthor
                    yield item
                    #dataObj = {'value' : review.xpath('div[@class="detailCont"]/h5/text()').extract(),
                    # 'key':review.xpath('div[@class="imageCont"]/a').extract()}
                    #print dataObj
                if litVal > 1:
                    nextEl.click()
                    self.val += 1
                if self.val > litVal:
                    break
                sleep(5)
            except Exception as e:
                print e
                break
        #self.driver.close()
