# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pynotifier import Notification
from pytz import timezone
from scrapy.exceptions import DropItem

from cowinchecker.telegramnotifier import CowinCheckerTelegramBot


class CowincheckerPipeline:
    def open_spider(self, spider):
        self.rows = [("date", "count", "age", "pincode", "center")]

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if ((adapter.get('available_capacity', 0) >= 5) and
            (spider.age == 0 or
             adapter.get('min_age_limit') <= spider.age)):
            self.rows.append((item.get("date"),
                              "{:0>3d}".format(item.get("available_capacity")),
                              str(item.get("min_age_limit")),
                              str(item.get("pincode")),
                              item.get("center_name")))
            return item
        else:
            raise DropItem(f"No slot available in {item.get('center_name')}")

    def close_spider(self, spider):
        stats = spider.crawler.stats.get_stats()
        scraped_count = stats.get('item_scraped_count', 0)
        if scraped_count > 0:
            curr_date = datetime.datetime.now(
                timezone("Asia/Calcutta")).strftime('%d-%m-%Y %H:%M:%S')
            description = ""
            for row in self.rows:
                description += " | ".join(row) + "\n"
            description += f"\n\nNotification Time - {curr_date}" + \
                           "\n\nBook on https://selfregistration.cowin.gov.in/"
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
