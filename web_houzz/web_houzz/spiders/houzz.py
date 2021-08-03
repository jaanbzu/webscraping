# -*- coding: utf-8 -*-
import scrapy
import requests

class HouzzSpider(scrapy.Spider):
    name = 'houzz'
    allowed_domains = ['houzz.com.au']
    def start_requests(self):
        yield scrapy.Request(
            url='https://www.houzz.com.au/professionals/searchDirectory?topicId=11949&query=Home+Builders&location=Melbourne%2C+Victoria&distance=50&sort=4',
            callback=self.parse,
        )

    def parse(self, response):
        for hotels in response.xpath("//*[@class='hz-pro-search-results__item']"):
            title = hotels.xpath(".//*[@itemprop='name']/text()").extract_first()
            link = hotels.xpath(".//*[@itemprop='url']/@href").extract_first()

            # yield {
            #     'title': title,
            #     'link': link,
            #     'link_web': link_web
            # }
            yield scrapy.Request(link,
                                 callback=self.parse_detail,
                                 meta={'title': title,
                                        'link': link})
            # yield scrapy.Request(link_2,
            #                      callback=self.parse_detail,
            #                      meta={'title': title,
            #                             'link_2': link_2})

        next_page = response.xpath("//*[@class='hz-pagination-link hz-pagination-link--next']/@href").get()
        yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_detail(self, response):
        title = response.meta['title']
        r = response.xpath("//*[@class='hz-profile-header__contact-info-item hz-track-me ']/@href").extract_first()
        website = requests.head(r, allow_redirects=True).url
        Phone_No = response.xpath("//*[@data-compid='Profile_Phone']/@href").extract_first()
        owner = response.xpath("//*[@class='profile-meta__val']/text()")[0].extract()

        yield {
                'title': title,
                'owner': owner,
                'Phone_No': Phone_No,
                'website': website
            }