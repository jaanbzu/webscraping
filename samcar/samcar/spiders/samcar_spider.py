import scrapy
from scrapy_splash import SplashRequest


class SamcarSpiderSpider(scrapy.Spider):
    name = 'samcar_spider'
    allowed_domains = ['www.samcar.org']
    # start_urls = ['http://www.samcar.org/']
    def start_requests(self):
        yield SplashRequest(url='https://www.samcar.org/membership/find-a-realtor/?lastname=A&page=1&PageSpeed=noscript', callback=self.parse)
    def parse(self, response):
        listings = response.xpath("//div[@class='item']")
        for listing in listings:
            name = listing.xpath(".//div[@class='membername']/a/text()").get()
            firm_name = listing.xpath(".//div[@class='firmname']/a/text()").get()
            address = listing.xpath("normalize-space(.//div[@class='memberaddr']/text())").get()
            phone = listing.xpath(".//div[@class='memberphone']/span/text()").get()
            mail = listing.css(".memberphone a::text").get()
            yield {
                'Name': name,
                'Firm_Name': firm_name,
                'Address': address,
                'Phone': phone,
                'Mail': mail
            }
        next_page = response.xpath("//a[@class='next']/@href").get()
        if next_page:
            yield SplashRequest(url=response.urljoin(next_page), callback=self.parse)
