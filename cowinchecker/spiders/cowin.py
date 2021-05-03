import datetime
import json
from urllib.parse import urlencode

import scrapy


class CowinSpider(scrapy.Spider):
    name = 'cowin'
    allowed_domains = ['cowin.gov.in', 'cdn-api.co-vin.in']
    base_url = 'https://cdn-api.co-vin.in/api/v2/'

    def __init__(self, state="Kerala", district="Ernakulam", *args, **kwargs):
        super(CowinSpider, self).__init__(*args, **kwargs)
        self.state = state
        self.district = district
        self.state_id = 17
        self.district_id = 307
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0",
            "Accept": "application/json, text/plain, */*"
        }

    def start_requests(self):
        query_params = {
            "district_id": self.district_id,
            "date": datetime.datetime.now().strftime('%d-%m-%Y')
        }
        search_url = self.base_url + \
            "appointment/sessions/public/calendarByDistrict" + "?" + \
            urlencode(query_params)
        yield scrapy.Request(search_url)

    def parse(self, response):
        centers = json.loads(response.text).get("centers", None)
        for center in centers:
            # center_id = center.center_id
            # name = center.name
            for session in center.get("sessions",None):
                if session.get("available_capacity") > 0:
                    print("date :", session.get("date"))
                    print("center id :", center.get("center_id"))
                    print("center name :", center.get("name"))
                    print("available capacity :", session.get("available_capacity"))
