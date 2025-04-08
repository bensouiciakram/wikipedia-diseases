import os 
import scrapy
from scrapy import Request 
from scrapy.loader import ItemLoader
from diseases.items import DiseasesItem
from scrapy.http.response.html import HtmlResponse


class InfosSpider(scrapy.Spider):
    """Scrapy spider for extracting epidemic information from Wikipedia.
    
    This spider scrapes the Wikipedia page listing historical epidemics and extracts:
    - Disease names
    - Dates of occurrence
    - Death tolls
    - Additional details from individual disease pages
    
    The extracted data is saved in JSON format.
    """
    name = 'infos'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ['http://en.wikipedia.org/']

    def __init__(self):
        """Initialize the spider by removing any existing output file."""
        try:
            os.remove('infos.json')
        except FileNotFoundError:
            pass

    start_urls = ['https://en.wikipedia.org/wiki/List_of_epidemics']    

    def parse(self, response: HtmlResponse):
        """Parse the main epidemics list page and extract basic information.
        
        Args:
            response (HtmlResponse): The response object from the initial request.
            
        Yields:
            Request: For each epidemic found, yields a request to the detail page.
        """
        # selecting the rows of the chronology table
        table_rows = response.xpath('//table[contains(@class,"wikitable sortable")]/tbody/tr')
        for row in table_rows[1:]:
            date = row.xpath('.//td[2]//text()').re('\d+')[0]
            epidemics = row.xpath('.//td[4]/a')
            for epidemic in epidemics:
                loader = ItemLoader(DiseasesItem(), epidemic)
                loader.add_xpath('disease', './text()')
                loader.add_value('date', date)
                loader.add_value('death_toll', row.xpath('.//td[5]/text()').get())
                url = epidemic.xpath('.//@href').get()
                loader.add_value('url', 'https://en.wikipedia.org/' + url)
                yield Request(
                    'https://en.wikipedia.org/' + url,
                    callback=self.parse_death,
                    meta={
                        'loader': loader
                    },
                    dont_filter=True
                )
                
    def parse_death(self, response: HtmlResponse):
        """Parse individual disease pages to extract detailed statistics.
        
        Args:
            response (HtmlResponse): The response object from the disease detail page request.
            
        Yields:
            Item: The fully populated disease item with all extracted information.
        """
        try:
            death_count = response.xpath('//th[contains(text(),"Deaths")]/following-sibling::td/text()')[0].get()
        except IndexError:
            death_count = 'N/A'
        try: 
            confirmed_cases = response.xpath('//th[contains(text(),"Frequency")]/following-sibling::td/text()')[0].get()
        except IndexError: 
            confirmed_cases = 'N/A'

        loader = response.meta['loader']
        loader.add_value('death', death_count)
        loader.add_value('confirmed_cases', confirmed_cases)
        yield loader.load_item()