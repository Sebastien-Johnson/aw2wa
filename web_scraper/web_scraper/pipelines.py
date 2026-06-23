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
        url = item['pdf_urls'][0]
        
        if url in self.urls_seen:
            raise DropItem(f'Duplicate: {url}')
        
        self.urls_seen.add(url)
        return item

class PdfScraperPipeline(FilesPipeline):
    def process_item(self, item, spider = None):
        return super().process_item(item, spider)
    
    def item_completed(self, results, item, info):
        
        file_paths = [x['path'] for ok, x in results if ok]

        if not file_paths:
            raise DropItem("No files downloaded")
        
        extracted_texts = []
        tables = []
        for file_path in file_paths:
            full_path = os.path.join(self.store.basedir, file_path)
            text = self.extract_with_pymupdf(full_path)
            tables = self.extract_tables_pymupdf(full_path)
            extracted_texts.append(text)

        item['extracted_texts'] = extracted_texts
        item['file_paths'] = file_paths
        item['tables'] = tables
        return item

    def extract_with_pymupdf(self, file_path):
        doc = pymupdf.open(file_path)
        text = ""

        for page_num in range(doc.page_count):
            page = doc[page_num]
            text += f"Page {page_num + 1}:\n"
            text += page.get_text()
            text += "\n" + "="*50 + "\n"

        doc.close()
        return text

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
        self.file = open("items.jsonl", "w")
    
    def close_spider(self):
        self.file.close()

    def process_item(self, item):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item
