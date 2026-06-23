import scrapy
import time
from urllib.parse import urljoin

class PdfSpider(scrapy.Spider):
    name = "pdf_spider"
    start_urls = ["https://drivenasa.com/results/?ee=1&eeFolder=NASA_Great_Lakes_Region%2F2025-Official-Results%2F2-Mid-Ohio-May-25&eeListID=2"]

    def parse(self, response):
        pdf_links = response.css('a[href$=".pdf"]::attr(href)').getall()

        for link in pdf_links:
            pdf_url = urljoin(response.url, link)
            yield {
                'pdf_url': [pdf_url],
                'source_url': response.url,
                'file_path' : [],
                'tables' : []
            }         

        for next_page in response.css('a[href*="page"]::attr(href)').getall():
            yield response.follow(next_page, self.parse)