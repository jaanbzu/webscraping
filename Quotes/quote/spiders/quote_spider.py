# -*- coding: utf-8 -*-
import scrapy


class QuoteSpiderSpider(scrapy.Spider):
    name = 'quote_spider'

    def start_requests(self):
        url= 'https://www.goodreads.com/quotes?page=1'

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for quote in response.selector.xpath("//div[@class='quote']"):
            yield {
                'text': quote.xpath(".//div[@class='quoteText']/text()[1]").extract_first(),
                'author': quote.xpath(".//div[@class='quoteText']/child::span[@class='authorOrTitle']/text()").extract_first(),
                'tag': quote.xpath(".//div[@class='greyText smallText left']/a/text()").extract()
            }

        next_page = response.selector.xpath("//li[@class='pagies']/child::a/@href").extract_first()
        if next_page is not None:
            next_page_link = response.urljoin(next_page)
            yield scrapy.Request(url=next_page_link, callback=self.parse)