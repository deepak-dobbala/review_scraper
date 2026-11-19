import os
from pathlib import Path
import logging

from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

class CrawlSpiderDemo(CrawlSpider):
    name = "quotes_crawl_spider"
    allowed_domains = ["quotes.toscrape.com"]

    start_urls = [
        "https://quotes.toscrape.com/"
    ]

    # rules is the set of 'Rule' objects that have the following properties link_extractor : LinkExtractor ; that parses the html and follows the url in the provided tag
    # follow : boolean ; this specifies if the CrawlSpider applies the same rules to the downstream pages or not
    rules = (
        Rule(
            link_extractor = LinkExtractor(
                restrict_css = "li.next a"
            ),
            callback = "parse_response",
            follow = True
        )
    )


    # Here we cannot override parse() function for Crawlspider because the class uses the parse function  to process the resposne with teh Rules and link followeres we configured
    # So to not interfere with that process we use a seperate function 
    def parse_response(self, response):
        self.logger.info(f"Gathering response from the page : {response.url}")
        self.logger.info(f"Page details : {response.body}")
        return


if __name__ == "__main__":
    logging.basicConfig(filename = "crawl_spider.log", level = "logging.INFO")

    process = CrawlerProcess(
        settings = {
            "FEEDS" : {
                "quotes.jsonl" : {
                    "format" : "jsonlines",
                    "encoding" : "utf8",
                    "overwrite" : True
                }
            },
            "LOG_LEVEL" : "INFO"
        }
    )

    process.crawl(CrawlSpider)

    process.start()