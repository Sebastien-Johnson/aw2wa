import scrapy
import os

from urllib.parse import urljoin, urlparse

class PdfSpider(scrapy.Spider):
    name = "pdf_spider"
    start_urls = ["https://my.scca.com/eweb/DynamicPage.aspx?WebCode=results&Site=scca#blackhole"]

    def parse(self, response):
        pdf_links = response.css('a[href$=".pdf"]::attr(href)').getall()

        for link in pdf_links:
            pdf_url = urljoin(response.url, link)
            yield {
                'file_urls': [pdf_url],
                'pdf_title': response.css('a[href="{}"]::text'.format(link)).get(),
                'source_page': response.url
            }

        next_page = response.css('a.next::attr(href)').get()
        if next_page:
            yield response.follow(next_page, self.parse) 