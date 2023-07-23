import scrapy
from scrapy import Request 
from urllib.parse import urljoin
from scrapy.loader import ItemLoader
from diseases.items import DiseasesItem
import os 
from scrapy.shell import inspect_response


class InfosSpider(scrapy.Spider):
    name = 'infos'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/']

    def __init__(self):
        try:
            os.remove('infos.json')
        except:
            pass

    start_urls = ['https://en.wikipedia.org/wiki/List_of_epidemics']    

    def parse(self, response):
        # selecting the rows of the chronology table
        table_rows = response.xpath('//table[contains(@class,"wikitable sortable")]/tbody/tr')
        for row in table_rows[1:]:
            date = row.xpath('.//td[2]//text()').re('\d+')[0]
            epidemics = row.xpath('.//td[4]/a')
            for epidemic in epidemics :
                loader = ItemLoader(DiseasesItem(),epidemic)
                loader.add_xpath('disease','./text()')
                loader.add_value('date',date)
                loader.add_value('death_toll',row.xpath('.//td[5]/text()').get())
                url = epidemic.xpath('.//@href').get()
                loader.add_value('url','https://en.wikipedia.org/' + url)
                yield Request(
                    'https://en.wikipedia.org/' + url,
                    callback = self.parse_death,
                    meta = {
                        'loader':loader
                    },
                    dont_filter =True
                )
                
    def parse_death(self,response):
        try:
            death_count = response.xpath('//th[contains(text(),"Deaths")]/following-sibling::td/text()')[0].get()
        except :
            death_count = 'N/A'
        try: 
            confirmed_cases = response.xpath('//th[contains(text(),"Frequency")]/following-sibling::td/text()')[0].get()
        except : 
            confirmed_cases = 'N/A'

        loader = response.meta['loader']
        loader.add_value('death',death_count)
        loader.add_value('confirmed_cases',confirmed_cases)
        yield loader.load_item()