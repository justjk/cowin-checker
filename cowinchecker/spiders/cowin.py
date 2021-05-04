import datetime
import json
import pathlib
from urllib.parse import urlencode

import scrapy
from cowinchecker.items import AvailableLocation


class CowinSpider(scrapy.Spider):
    name = 'cowin'
    allowed_domains = ['cowin.gov.in', 'cdn-api.co-vin.in']
    base_url = 'https://cdn-api.co-vin.in/api/v2/'

    custom_settings = {
        'FEEDS': {
            pathlib.Path('items.csv'):{
                'format': 'csv'
            }
        }
    }

    def __init__(self, state="Kerala", district="Ernakulam", *args, **kwargs):
        super(CowinSpider, self).__init__(*args, **kwargs)
        self.state = state
        self.district = district
        self.state_id = 17
        self.district_id = 516

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
                yield location
