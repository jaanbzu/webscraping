import scrapy
import json
from ..items import RightmoveItem


class HomesSpider(scrapy.Spider):
    name = 'homes'
    allowed_domains = ['www.rightmove.co.uk']
    cookies = {
        'permuserid': '200827EBEIURI99TXWQL4RWMW1R2U8JF',
        'beta_optin': 'N:65:-1',
        'RM_Register': 'C',
        'TS016a0c54': '012f990cd3eeb60c00268fc4ca7b5399d427bf13617d9d749e46cb6579d29c853a02734030b5c91f85df4d2647ce8243f6121be604',
        '_gaRM': 'GA1.3.2031638428.1598557384',
        '_gaRM_gid': 'GA1.3.437113537.1598557384',
        '__utma': '6980913.2026740268.1598557385.1598557385.1598557385.1',
        '__utmc': '6980913',
        '__utmz': '6980913.1598557385.1.1.utmcsr=google^|utmccn=(organic)^|utmcmd=organic^|utmctr=(not^%^20provided)',
        '__utmt': '1',
        'cdUserType': 'none',
        'TS01a07bd2': '012f990cd309b1a5166625b640b0ae7b3dd792c7f3f271ed74c41f7d2cde4233e72e6dc80aeaa4345f6f093bf020d6e0da99be051c44ec201dedf311920d422558186b97c8891556909ae2da34ba6e478ded6ba5023b948f24b6f51bebaac2d43f46979aa44a37ed5195e6c5020cac3f96177ad419f22e0130c781ffb5cf067534faa1f58e',
        '__utmv': '6980913.^|1=source=google-seo=1^^2=keyword=not-provided=1^^33=Login^%^20Register^%^20Modal^%^20Test=T=1',
        '__utmb': '6980913.6.8.1598557444080',
        'svr': '1708',
        'TS01ec61d1': '012f990cd370dc1702fab2982f4fc3ce97306607b7f271ed74c41f7d2cde4233e72e6dc80aa859167fef3c96a6d877ef02a77bb96c8f654a65627221e866368822640214365fec2f318a1d3134b6f0279dd57713ff',
        'rmsessionid': '5f4fd4c7-446f-4835-903a-99cd7f55395d',
        'lastViewedFeaturedProperties': '94514486',
        'JSESSIONID': '0B584B2F2D3CA6A64FD093B1C623A02F',
        'TS019c0ed0': '012f990cd3b5e52543bf21042b1386a3e08658d9d6f271ed74c41f7d2cde4233e72e6dc80ac312b6a90abdcf279938c6d47c718f490d8820a2c83cb9ef7545c5c8cfcaaf39b62ad0746b48b8414e01210f1ac39ed61d2f65b65a6d1cfaedade7a2f94722865708d77f16c806a7a6f0cd3880895c1b',
        'TS01826437': '012f990cd30a79d608a179eb29e477519aa989bc1cf271ed74c41f7d2cde4233e72e6dc80aeaa4345f6f093bf020d6e0da99be051c44ec201dedf311920d422558186b97c8891556909ae2da34ba6e478ded6ba5023b948f24b6f51bebaac2d43f46979aa44a37ed5195e6c5020cac3f96177ad4198d8a56b57250f9ab7c60c66cfb24cc61ba85b021686c2e6b798d312b8edf54a0088f64c98916245af5ff8aeaf3af0b13',
        'OptanonConsent': 'isIABGlobal=false^&datestamp=Fri+Aug+28+2020+00^%^3A46^%^3A45+GMT^%^2B0500+(Pakistan+Standard+Time)^&version=5.11.0^&landingPath=NotLandingPage^&groups=1^%^3A1^%^2C3^%^3A1^%^2C4^%^3A0^&AwaitingReconsent=false',
        '_gat_UA-3350334-63': '1',
    }


# headers = {
#     'Connection': 'keep-alive',
#     'Accept': 'application/json, text/javascript',
#     'X-Requested-With': 'XMLHttpRequest',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36',
#     'Content-Type': 'application/x-www-form-urlencoded',
#     'Sec-Fetch-Site': 'same-origin',
#     'Sec-Fetch-Mode': 'cors',
#     'Sec-Fetch-Dest': 'empty',
#     'Referer': 'https://www.rightmove.co.uk/property-to-rent/find.html?locationIdentifier=REGION^%^5E94316^&index=24^&propertyTypes=^&includeLetAgreed=false^&mustHave=^&dontShow=^&furnishTypes=^&keywords=',
#     'Accept-Language': 'en-US,en;q=0.9',
# }
start_urls = [
    'https://www.rightmove.co.uk/api/_search?locationIdentifier=REGION%5E94316&numberOfPropertiesPerPage=24&radius=0.0&sortType=6&includeLetAgreed=false&viewType=LIST&channel=RENT&areaSizeUnit=sqft&currencyCode=GBP&isFetching=false&index=24']
def start_requsts(self):
    for url in self.start_urls:
        yield scrapy.Request(
            url,
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            cookies = self.cookies
        )
def parse(self, response):
    json_resp = json.loads(response.body)
    houses = json_resp.get('properties')
    for house in houses:
        house_item = RightmoveItem()
        house_item['address'] = house.get('displayAddress')
        house_item['price'] = house.get('price').get('amount')
        house_item['name'] = house.get('customer').get('branchDisplayName')
        house_item['phone'] = house.get('customer').get('contactTelephone')
        yield house_item
