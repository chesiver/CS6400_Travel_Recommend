import scrapy
from scrapy.http import Request


class Site(scrapy.Item):
    country = scrapy.Field()
    city = scrapy.Field()
    name = scrapy.Field()
    type = scrapy.Field()
    intro = scrapy.Field()

class CountrySpider(scrapy.Spider):

    name = 'country_wiki_travel'

    def start_requests(self):
        urls = [
            'https://wikitravel.org/en/A%E2%80%93Z_list_of_countries'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for country_name in response.css('#mw-content-text > table li a::text').extract():
            country_name = country_name.strip()
            if len(country_name) == 0: continue
            countryUrl = 'https://wikitravel.org/en/' + country_name
            print('visiting country ' + country_name)
            print(countryUrl)
            print('-------------------')
            request = Request(url=countryUrl, callback=self.parse_country_page,
                              meta={'country_name': country_name})
            yield request


    def parse_country_page(self, response):
        country_name = response.meta['country_name']
        for city_name in response.xpath('//*[@id="mw-content-text"]/table/tr/td/ul[preceding-sibling::h2[1]/span[1]/text()="Cities" and following-sibling::h2[1]/span[1]/text()="Other destinations"]/li/a/text()').extract():
            city_name = city_name.strip()
            if len(city_name) == 0: continue
            city_url = 'https://wikitravel.org/en/' + city_name
            print('visiting country ' + city_name)
            print(city_url)
            print('-------------------')
            request = Request(url=city_url, callback=self.parse_city_page,
                              meta={'country_name': country_name, 'city_name': city_name})
            yield request


    def parse_city_page(self, response):
        country_name = response.meta['country_name']
        city_name = response.meta['city_name']
        for site in response.xpath('//*[@id="mw-content-text"]/table/tr/td/ul[preceding-sibling::h2[1]/span[1]/text()="See" and following-sibling::h2[1]/span[1]/text()="Do"]/li'):
            site_name = site.xpath('.//b/text()').extract_first()
            if site_name:
                site_intro_paragraph = site.xpath('.//text()').extract()
                if type(site_intro_paragraph) is list:
                    intro = ' '.join(site_intro_paragraph)
                elif type(site_intro_paragraph) is str:
                    intro = site_intro_paragraph
                else:
                    intro = ' '
                yield Site(country=country_name, city=city_name, name=site_name, intro=intro)
        for site in response.xpath('//*[@id="mw-content-text"]/table/tr/td/ul[preceding-sibling::h2[1]/span[1]/text()="See" and following-sibling::h2[1]/span[1]/text()="Do"]/li/span[@class="vcard"]'):
            site_name = site.xpath('.//span[@class="fn org"]/text()').extract_first()
            if site_name:
                site_intro_paragraph = site.xpath('.//span[@class="description"]/text()').extract()
                if type(site_intro_paragraph) is list:
                    intro = ' '.join(site_intro_paragraph)
                elif type(site_intro_paragraph) is str:
                    intro = site_intro_paragraph
                else:
                    intro = ' '
                yield Site(country=country_name, city=city_name, name=site_name, intro=intro)