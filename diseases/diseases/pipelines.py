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
        date = int(re.findall('\d+',item['date'][0])[0])
        
        if date < 1960:
            raise DropItem

        if item['death'][0] == 'N/A':
            item['death'][0] = item['death_toll'][0]
        else:
            if item['disease'][0].lower() in self.diseases:
                raise DropItem                    
        self.diseases.add(item['disease'][0].lower())
        return item
    
