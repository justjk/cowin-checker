# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pynotifier import Notification
from scrapy.exceptions import DropItem


class CowincheckerPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('available_capacity') > 0:
            return item
        else:
            raise DropItem(f"No slot available in {item.get('center_name')}")
        return item

    def close_spider(self, spider):
        stats = spider.crawler.stats.get_stats()
        scraped_count = stats.get('item_scraped_count', 0)
        if scraped_count > 0:
            Notification(
                title=f"Available Centers - {scraped_count}",
                description='Check items.csv',
                # icon_path='path/to/image/file/icon.png', # On Windows .ico is required, on Linux - .png
                duration=5,                              # Duration in seconds
                urgency='normal'
            ).send()
