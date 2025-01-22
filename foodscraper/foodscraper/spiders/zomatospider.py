import scrapy
from foodscraper.items import FoodscraperItem

class ZomatospiderSpider(scrapy.Spider):
    name = "zomatospider"
    allowed_domains = ["zomato.com"]
    start_urls = ["https://www.zomato.com/phagwara/order-food-online?delivery_subzone=30561"]
    custom_settings = {
        'FEEDS': {
            'zomato_data.csv': {
                'format': 'csv',
                'encoding': 'utf-8',
                'overwrite': True
            }
        },
        'FEED_EXPORT_FIELDS': ['restraunt_name', 'location', 'contact', 'dining_ratings', 'delivery_ratings','menu_name','menu_description','menu_price','menu_rating']
    }

    def parse(self, response):
        # Extract all restaurant links from the listing page
        restaurant_links = response.css('a.sc-hqGPoI::attr(href)').getall()
        base_url = "https://www.zomato.com"
        for link in set(restaurant_links):
            url = base_url + link
            yield response.follow(url, self.parse_restaurant)

    def parse_restaurant(self, response):
        # Extract restaurant details
        restraunt_name = response.css('h1.sc-7kepeu-0::text').get(default='N/A')
        location = response.css('a.sc-clNaTc::text').get(default='N/A')
        contact = response.xpath('//a[contains(@href, "tel")]/text()').get(default=-1)
        ratings = response.css('div.sc-1q7bklc-1::text').getall()
        dining_ratings = ratings[0].strip() if len(ratings) > 0 and ratings[0].strip() else -1
        delivery_ratings = ratings[1].strip() if len(ratings) > 1 and ratings[1].strip() else -1

        # Extract menu items
        menu_items = response.css('section.sc-gOhSNZ.fXfmoU div.sc-jhLVlY.cFNHph')

        # Initialize and yield item for each menu
        for menu in menu_items:
            item = FoodscraperItem()
            item['restraunt_name'] = restraunt_name
            item['location'] = location
            item['contact'] = contact
            item['dining_ratings'] = dining_ratings
            item['delivery_ratings'] = delivery_ratings
            item['menu_name'] = menu.css('h4.sc-fuzEkO::text').get(default='N/A')
            item['menu_price'] = menu.css('span.sc-17hyc2s-1.cCiQWA::text').get(default=-1)
            item['menu_rating'] = menu.css('div.sc-hfsWMF.cOzgMB::attr(title)').get(default=-1)
            item['menu_description'] = menu.css('p.sc-cGCqpu.bWHESZ::text').get(default='N/A')

            yield item


