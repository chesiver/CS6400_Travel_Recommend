import scrapy

class CountrySpider(scrapy.Spider):

    name = 'country'

    def start_requests(self):
        urls = [
            'https://www.lonelyplanet.com/places'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for country in response.css('div.grid-wrapper--10 a.card--list h3.card--list__name::text').extract():
            yield {
                'name': country[1:-1]
            }