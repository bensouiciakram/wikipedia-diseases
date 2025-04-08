# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
import re 

class DiseasesPipeline:
    """Scrapy pipeline for processing and filtering disease items.
    
    This pipeline performs the following operations:
    - Filters out diseases that occurred before 1960
    - Handles missing death count data by using the death toll value
    - Ensures disease entries are unique (case-insensitive)
    - Maintains a set of processed diseases to prevent duplicates
    """
    
    def __init__(self):
        """Initialize the pipeline with an empty set to track processed diseases."""
        self.diseases = set()

    def process_item(self, item, spider):
        """Process each item through the pipeline filters and transformations.
        
        Args:
            item (DiseasesItem): The scraped item containing disease information
            spider (scrapy.Spider): The spider that generated this item
            
        Raises:
            DropItem: If the disease occurred before 1960 or is a duplicate
            
        Returns:
            DiseasesItem: The processed item with potentially modified death count
        """
        date = int(re.findall('\d+', item['date'])[0])
        if date < 1960:
            raise DropItem(f"Disease from {date} is too old (pre-1960)")
            
        if item['death'] == 'N/A':
            item['death'] = item['death_toll']
        else:
            if item['disease'].lower() in self.diseases:
                raise DropItem(f"Duplicate disease found: {item['disease']}")
                
        self.diseases.add(item['disease'].lower())
        return item