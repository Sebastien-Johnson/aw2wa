# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import os
import pymupdf
import json
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.exceptions import DropItem


class DuplicateUrls:
    def __init__(self):
        self.urls_seen = set()
        self.filename = 'seen_urls.txt'

    def open_spider(self, spider):
        if os.path.exists(self.filename):
            with open(self.filename, 'r') as f:
                self.urls_seen = set(line.strip() for line in f)
            #spider.logger.info(f'Loaded {len(self.urls_seen)} seen URLs')
    
    def close_spider(self, spider):
        with open(self.filename, 'w') as f:
            for url in self.urls_seen:
                f.write(url + '\n')
        #spider.logger.info(f'Saved {len(self.urls_seen)} URLs')
    
    def process_item(self, item, spider):
        url = item['pdf_url'][0]
        
        if url in self.urls_seen:
            raise DropItem(f'Duplicate: {url}')
        
        self.urls_seen.add(url)
        return item

class PdfScraperPipeline(FilesPipeline):
    def file_path(self, request, response = None, info = None, *, item = None):
        region_folder = request.url.split("/")[-4]
        item["region"] = region_folder[5:]
        year_folder = request.url.split("/")[-3]
        item["year"] = year_folder[:4]
        event_folder = request.url.split("/")[-2]
        item["track_event"] = event_folder
        race_file = request.url.split("/")[-1]
        new_filename = f"{region_folder}/{year_folder}/{event_folder}/{race_file}"
        return new_filename
    
    def process_item(self, item, spider = None):
        return super().process_item(item, spider)
    
    def item_completed(self, results, item, info):
        
        file_path = [x['path'] for ok, x in results if ok]

        if not file_path:
            raise DropItem("No files downloaded")
        
        
        tables = []
        for path in file_path:
            full_path = os.path.join(self.store.basedir, path)
            tables = self.extract_tables_pymupdf(full_path)
            

        item['file_path'] = file_path
        item['tables'] = tables
        return item

    def extract_tables_pymupdf(self, file_path):
        doc = pymupdf.open(file_path)
        tables = []

        for page in doc:
            page_tables = page.find_tables()
            for table in page_tables:
                tables.append(table.extract())

        doc.close()
        return tables
    
class JsonWritePipeline:
    def open_spider(self):
        self.file = open("items.jsonl", "a")
    
    def close_spider(self):
        self.file.close()

    def process_item(self, item):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
