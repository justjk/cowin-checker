import datetime
import json
from urllib.parse import urlencode

import scrapy
from items import AvailableLocation


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
            for session in center.get("sessions", None):
                location = AvailableLocation(center_id=center.get("center_id"),
                                             center_name=center.get("name"),
                                             date=session.get("date"),
                                             available_capacity=session.get(
                                                 "available_capacity"),
                                             min_age_limit=session.get(
                                                 "min_age_limit"))
