import scrapy


class CowinSpider(scrapy.Spider):
    name = 'cowin'
    allowed_domains = ['cowin.gov.in']
    start_urls = ['http://cowin.gov.in/']

    def parse(self, response):
        pass
