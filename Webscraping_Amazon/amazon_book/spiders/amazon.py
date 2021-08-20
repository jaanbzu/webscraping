# -*- coding: utf-8 -*-
import scrapy
from amazon_book.items import AmazonBookItem
from scrapy.loader import ItemLoader


class ShopSpider(scrapy.Spider):
    name = 'amazon'
    def start_requests(self):
        url= 'https://www.amazon.com/s?i=stripbooks&bbn=283155&rh=n%3A283155%2Cp_n_publication_date%3A1250226011%2Cp_n_feature_browse-bin%3A2656020011&dc&page=1&fst=as%3Aoff&qid=1571686718&rnid=618072011&ref=sr_pg_1'
        yield scrapy.Request(url=url, callback=self.parse)
    def parse(self, response):
        for books in response.selector.xpath(".//div[@class='s-include-content-margin s-border-bottom']"):
            loader= ItemLoader(item=AmazonBookItem(), selector=books, response=response)
            loader.add_xpath('Title', ".//span[@class='a-size-medium a-color-base a-text-normal']/text()")
            loader.add_css('Author', ".a-color-secondary .a-size-base+ .a-size-base , .a-color-secondary .a-size-base.a-link-normal")
            loader.add_xpath('Price', ".//div[@class='a-section a-spacing-none a-spacing-top-small']/div[@class='a-row a-size-base a-color-base']/div[@class='a-row']/a[@class='a-size-base a-link-normal s-no-hover a-text-normal']/span[@class='a-price']/child::span[@class='a-offscreen']//text()")
            loader.add_xpath('Image_Link', ".//div[@class='a-section aok-relative s-image-fixed-height']//img/@src")
            yield loader.load_item()