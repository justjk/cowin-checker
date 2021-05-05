# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


import datetime

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pynotifier import Notification
from scrapy.exceptions import DropItem


class CowincheckerPipeline:
    def open_spider(self, spider):
        self.file = open('items.csv', 'w')

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if ((adapter.get('available_capacity', 0) > 0) and
            (spider.age == 0 or
             adapter.get('min_age_limit') <= spider.age)):
            return item
        else:
            raise DropItem(f"No slot available in {item.get('center_name')}")
        return item

    def close_spider(self, spider):
        self.file.close()
        stats = spider.crawler.stats.get_stats()
        scraped_count = stats.get('item_scraped_count', 0)
        if scraped_count > 0:
            curr_date = curr_date = datetime.datetime.now().strftime(
                '%d-%m-%Y %H:%M:%S')
            Notification(
                title=f"Available Centers - {scraped_count}",
                description=f"Check items.csv - {curr_date}",
                duration=5,
                urgency='normal'
            ).send()
