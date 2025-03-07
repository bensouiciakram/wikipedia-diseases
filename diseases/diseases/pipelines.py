# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re 

class DiseasesPipeline:
    def __init__(self):
        self.diseases = set()

    def process_item(self, item, spider):
        date = int(re.findall('\d+',item['date'])[0])
        if date < 1960:
            raise DropItem
        if item['death'] == 'N/A':
            item['death'] = item['death_toll']
        else:
            if item['disease'].lower() in self.diseases:
                raise DropItem                    
        self.diseases.add(item['disease'].lower())
        return item
    
