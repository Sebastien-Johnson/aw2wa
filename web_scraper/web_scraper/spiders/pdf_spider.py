import scrapy
from web_scraper.items import RaceDataItem
from urllib.parse import urljoin

class PdfSpider(scrapy.Spider):
    name = "pdf_spider"
    start_urls = ["https://drivenasa.com/results/?ee=1&eeListID=2"]


    def parse(self, response):
        pdf_links = response.css('a[href$=".pdf"]::attr(href)').getall()
        
        for link in pdf_links:
            pdf_url = urljoin(response.url, link)
            item = RaceDataItem()
            item["pdf_url"] = [pdf_url]
            item["source_url"] = response.url
            yield item

        for next_page in response.css('a[href*="results"]::attr(href)').getall():
            if next_page[-4:] != ".pdf":
                print(next_page)
                yield response.follow(next_page, self.parse)
        