






import scrapy
from scrapy.crawler import CrawlerProcess


class MySpider(scrapy.Spider):
    # Your spider definition
    ...

class Crawler:
    def crawl(self):
        process = CrawlerProcess(settings={
            "FEEDS": {
                "items.json": {"format": "json"},
            },
        })

        process.crawl(MySpider)
        process.start()  # the script will block here until the crawling is finished
