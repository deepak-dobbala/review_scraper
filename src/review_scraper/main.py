import sys
import scrapy
from bs4 import BeautifulSoup

class DemoScraper(scrapy.Spider):
    name="quotes"

    async def start(self):
        # Scrapy hits these url when started with the cmd $scrapy runspider main.py -o output.jsonl [The output flags ]
        start_urls=[
            "https://quotes.toscrape.com/",
            "https://quotes.toscrape.com/page/2",
        ]

        # SCrapy does not  use threads instead  of which it sends out sync await requests and it does not waste any computing potential on watiting for the ressponse
        index=0
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse, meta={"page_id":index})
            index+=1

    def parse(self, response):
        html_soup = BeautifulSoup(response.body,'html.parser')
        print(html_soup.prettify())

