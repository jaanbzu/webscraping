# -*- coding: utf-8 -*-
import scrapy
import json
from pprint import pprint


class SchoolSpider(scrapy.Spider):
    name = 'school'
    allowed_domains = ['directory.ntschools.net']

    headers = {
        'Accept': 'application/json',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Cookie': 'BIGipServerdirectory.ntschools.net_443.app~directory.ntschools.net_443_pool=360972810.20480.0000',
        'Host': 'directory.ntschools.net',
        'Referer': 'https://directory.ntschools.net/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36',
        'X-Requested-With': 'Fetch',
    }
    start_urls = ['https://directory.ntschools.net/api/System/GetAllSchools']
    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        raw_data = json.loads(response.text)
        for data in raw_data:
            school_id = data.get('itSchoolCode')
            next_url = ("https://directory.ntschools.net/api/System/GetSchool?itSchoolCode={}").format(school_id)
            yield response.follow(next_url, callback=self.parse_detail, headers=self.headers)

    def parse_detail(self, response):
        result = json.loads(response.body)
        # with open('raw_data_string.json', 'w') as f:
        #     json.dump(result, f)
        name = result.get('name')
        address = result.get('physicalAddress').get('displayAddress')
        postalAddress = result.get('postalAddress').get('displayAddress')
        phone = result.get('telephoneNumber')
        facsimileTelephoneNumber = result.get('facsimileTelephoneNumber')
        email = result.get('mail')
        web = result.get('uri')
        yield {
            'name': name,
            'address': address,
            'postalAddress': postalAddress,
            'phone': phone,
            'facsimileTelephoneNumber': facsimileTelephoneNumber,
            'email': email,
            'web': web
        }
       
        
