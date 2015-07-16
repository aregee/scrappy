from scrapy import Spider
from scrapy.selector import Selector
from bricks.items import BricksItem, BrickReviewItem
from bricks.pipelines import MongoDBPipeline
from scrapy.selector import HtmlXPathSelector
from selenium import webdriver
from time import sleep
import selenium
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (
    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/37.0.2062.120 Safari/537.36;"
)
#driver = webdriver.PhantomJS(
#    executable_path='/usr/local/bin/phantomjs', desired_capabilities=dcap)
driver = webdriver.Firefox()
mdb = MongoDBPipeline(collection_name='baseUrls')
get_all = mdb.get_all()


class BrickSpider(Spider):
    name = "bricked"
    allowed_domains = ["magicbricks.com"]
    start_urls = [
        "http://www.magicbricks.com/locality/New-Delhi-Locality-Review.htm",
        "http://www.magicbricks.com/locality/Noida-Locality-Review.htm",
        "http://www.magicbricks.com/locality/Gurgaon-Locality-Review.htm",
        "http://www.magicbricks.com/locality/Ghaziabad-Locality-Review.htm",
        "http://www.magicbricks.com/locality/Bangalore-Locality-Review.htm",
        "http://www.magicbricks.com/locality/Mumbai-Locality-Review.htm",
    ]

    def parse(self, response):
        locations = Selector(response).xpath(
            '//div[@class=\"maincantent\"]/div/div')
        for loc in locations:
            item = BricksItem()
            item['title'] = loc.xpath(
                'div[@class=\"boxcon\"]/div/div[@class=\"infoe\"]/text()').extract()[0]
            item['url'] = loc.xpath(
                'div[@class=\"boxcon\"]/a/@href').extract()[0]
            yield item


class BrickReviewSpider(Spider):
    name = "bricks"
    allowed_domains = ["magicbricks.com"]
#    letItbe =  [(str(x['url']).replace('advice.magicbricks.com', 'magicbricks.com')) for x in get_all.find()]
    start_urls = [
        "http://advice.magicbricks.com/Indirapuram-in-Ghaziabad-Overview"]

    def parse(self, response):
        item = BricksItem()
        pageParsed = Selector(response).xpath(
            '//div[@id="localityProfileWrapper"]')
        reviewTitle = ", ".join(
            pageParsed.xpath('//*[@id="localityProfileMsg"]/h1/text()').extract())
        reviewArea = ", ".join(pageParsed.xpath(
            '//div[@id="localityProfileWrapper"]/div[3]/div[4]/div[1]/div[1]/span/h3/text()').extract())
        reviewObj = pageParsed.xpath(
            "//div[@id=\"localityProfileWrapper\"]/div[3]/div[2]/span[2]/text()").extract()[0]
        if reviewTitle:
            item['title'] = reviewTitle
            item['url'] = response.url
        if reviewObj:
            item['review_body'] = reviewObj
        if reviewArea:
            item['locality'] = reviewArea
        yield item
        print reviewTitle
        print reviewArea
        print reviewObj
        print response.url

# http://www.magicbricks.com/real-estate-property-reviews/Aashirwaad-Chowk-in-New-Delhi#reviewResult


class DepricatedSpider(Spider):
    name = "deprireviewer"
    allowed_domains = ["magicbricks.com"]
    letItbe = [(str(x['url']).replace('advice.magicbricks.com', 'magicbricks.com'))
               for x in get_all.find()]
#    letItbe =  [str(x['url']) for x in get_all.find()]
    # ['http://www.magicbricks.com/Aashirwaad-Chowk-in-New-Delhi-Overview']#letItbe
    start_urls = letItbe

    def parse(self, response):
        item = BrickReviewItem()
        parseItem = {}
        print "starting phantomjs"
        driver.get(response.url)
        source = driver.page_source

        sou2 = source.encode('ascii', 'ignore')
        # print sou2
        reviewObj = Selector(text=sou2)
        #item['title'] = str(reviewObj.xpath("//*[@id=\"localityProfileMsg\"]/h1/text()").extract()[0])
        parseItem['review'] = {"review_url": str("http://magicbricks.com" + reviewObj.xpath('//*[@id=\"localityProfileNav\"]/ul/*[@id=\"localityReviews\"]/a/@href').extract(
        )[0]), 'count': reviewObj.xpath("//*[@id=\"localityProfileNav\"]/ul/*[@id=\"localityReviews\"]/a/div[2]/text()").extract()[0]}
        reviewTitle = ", ".join(
            reviewObj.xpath('//*[@id="localityProfileMsg"]/h1/text()').extract())
        reviewArea = ", ".join(reviewObj.xpath(
            '//div[@id="localityProfileWrapper"]/div[3]/div[4]/div[1]/div[1]/span/h3/text()').extract())
        reviewTxt = reviewObj.xpath(
            "//div[@id=\"localityProfileWrapper\"]/div[3]/div[2]/span[2]/text()").extract()[0]
        parseItem['rating'] = reviewObj.xpath(
            "//*[@id=\"ratingBox\"]/div/div[1]/div[2]/div[1]/p/span[1]/strong/text()").extract()[0]
        parseItem['top-rated-categories'] = reviewObj.xpath(
            '//*[@id=\"ratingBox\"]/div/div[1]/div[2]/div[2]/ul/li/div/text()').extract()
        months = reviewObj.xpath("//*[@id=\"mainResultDiv\"]/div/div[1]/ul/li/div[@class=\"titleData\"]/text()").extract()
        prices = reviewObj.xpath("//*[@id=\"mainResultDiv\"]/div/div[1]/ul/li/div[@class=\"descriptionData\"]/text()").extract()
        trends = dict(zip(months, prices))
        n1 = reviewObj.xpath("//*[@id=\"mainResultDiv\"]/div/div[1]/ul/li[@class=\"foot\"]/span/text()").extract()[0]

        n2 = reviewObj.xpath("//*[@id=\"mainResultDiv\"]/div/div[1]/ul/li[@class=\"foot\"]/span/img/@src").extract()[0]
        print "fucking >>>>>REFADASD FORMDAS HERERe"
        print n1.split('&')
        n2 = n2.split('/')
        n2 = n2.pop()
        print n2
        trends['history'] = { str(reviewObj.xpath("//*[@id=\"mainResultDiv\"]/div/div[1]/ul/li[@class=\"foot\"]/text()").extract()[0]): n1+n2 }
        parseItem['price_trend'] = trends
        parseItem['locality_recomended_for'] = reviewObj.xpath("//*[@id=\"ratingBox\"]/div/p/span/strong/text()").extract()
        clickableElms = reviewObj.xpath("//*[@id=\"poimap\"]/div[2]/div[2]/ul/li")
        if reviewTitle:
            item['title'] = reviewTitle
            item['url'] = response.url
        if reviewTxt:
            item['review_body'] = reviewTxt
        if reviewArea:
            item['locality'] = reviewArea
        item['meta_data'] = parseItem
        yield item
