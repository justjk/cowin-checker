import datetime
import json
import pathlib
from urllib.parse import urlencode

import scrapy
from cowinchecker.items import AvailableLocation
from pytz import timezone


class CowinSpider(scrapy.Spider):
    name = 'cowin'
    allowed_domains = ['cowin.gov.in', 'cdn-api.co-vin.in']
    base_url = 'https://cdn-api.co-vin.in/api/v2/'

    custom_settings = {
        'FEEDS': {
            pathlib.Path('output/items.csv'): {
                'format': 'csv',
                'overwrite': True,
                'fields': ['date', 'center_name', 'available_capacity',
                           'min_age_limit', 'vaccine', "district_name"]
            }
        }
    }

    def __init__(self, district_ids="307", age=None, *args, **kwargs):
        super(CowinSpider, self).__init__(*args, **kwargs)

        self.district_ids = district_ids.split(',')
        curr_date = datetime.datetime.now(timezone("Asia/Calcutta"))
        self.search_dates = [curr_date.strftime('%d-%m-%Y')]
        for i in range(1, 4):
            curr_date = curr_date + datetime.timedelta(days=7)
            self.search_dates.append(curr_date.strftime('%d-%m-%Y'))
        self.age = int(age or 0)

    def start_requests(self):
        for district_id in self.district_ids:
            for date in self.search_dates:
                query_params = {
                    "district_id": district_id,
                    "date": date
                }
                search_url = self.base_url + \
                    "appointment/sessions/calendarByDistrict" + "?" + \
                    urlencode(query_params)
                yield scrapy.Request(search_url)

    def parse(self, response):
        centers = json.loads(response.text).get("centers", None)
        for center in centers:
            for session in center.get("sessions", None):
                location = AvailableLocation(state_name=center.get(
                                                "state_name"),
                                             district_name=center.get(
                                                 "district_name"),
                                             center_id=center.get("center_id"),
                                             center_name=center.get("name"),
                                             fee_type=center.get("fee_type"),
                                             date=session.get("date"),
                                             available_capacity=session.get(
                                                 "available_capacity"),
                                             min_age_limit=session.get(
                                                 "min_age_limit"),
                                             vaccine=session.get("vaccine"),
                                             slots=session.get("slots"))
                yield location
