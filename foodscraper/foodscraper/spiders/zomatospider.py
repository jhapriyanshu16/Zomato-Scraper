import scrapy


class ZomatospiderSpider(scrapy.Spider):
    name = "zomatospider"
    allowed_domains = ["www.zomato.com"]
    start_urls = ["https://www.zomato.com/phagwara/asf-american-style-fried-phagwara-locality/order"]

    def parse(self, response):
        pass
