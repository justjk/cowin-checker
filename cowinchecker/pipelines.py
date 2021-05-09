# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pynotifier import Notification
from scrapy.exceptions import DropItem

from cowinchecker.telegramnotifier import CowinCheckerTelegramBot


class CowincheckerPipeline:
    def open_spider(self, spider):
        self.district_names = set()
        self.available_dates = set()

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if ((adapter.get('available_capacity', 0) > 0) and
            (spider.age == 0 or
             adapter.get('min_age_limit') <= spider.age)):
            self.available_dates.add(item.get("date"))
            self.district_names.add(item.get("district_name"))
            return item
        else:
            raise DropItem(f"No slot available in {item.get('center_name')}")

    def close_spider(self, spider):
        stats = spider.crawler.stats.get_stats()
        scraped_count = stats.get('item_scraped_count', 0)
        if scraped_count > 0:
            curr_date = datetime.datetime.now().strftime(
                '%d-%m-%Y %H:%M:%S')
            description = f"Available Slots - {scraped_count} " + \
                          "(Center + Date).\n" + \
                          f"Districts - {self.district_names}\n" + \
                          f"\nDates - {self.available_dates}\n\n" + \
                          f"Notification Time - {curr_date}\n\n" + \
                          "Book on https://selfregistration.cowin.gov.in/"
            Notification(
                title=f"Available Centers - {scraped_count}",
                description=description,
                duration=5,
                urgency='normal'
            ).send()
            try:
                CowinCheckerTelegramBot.send_notification(text=description)
            except Exception as e:
                spider.logger.error(
                    f'Error sending Telegram notification: {e}')
