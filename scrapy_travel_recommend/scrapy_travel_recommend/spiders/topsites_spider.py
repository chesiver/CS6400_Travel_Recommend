import scrapy
import json

class TopSitesSpider(scrapy.Spider):

    name = 'top_sites'

    def start_requests(self):
        urls = []
        with open('country.json') as data_file:
            countries = json.load(data_file)
        for country in countries:
            urls.append('https://www.lonelyplanet.com/' + country['name'].lower());
        print('-------------------------------------------')
        print (urls)
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):
        for item in response.css('div.SightsList-item'):
            yield {
                'country': response.request.url.split('/')[-1],
                'name': item.xpath('.//a/div[2]/h5/text()').extract()
            }
            print ('-------------------------------------------')
            print (item.xpath('.//a/div[2]/h5/text()').extract())
