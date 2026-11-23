import os
from pathlib import Path
import logging

from scrapy.spiders import CrawlSpider, Rule
from scrapy.crawler import CrawlerProcess
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup


class CrawlSpiderDemo(CrawlSpider):

    name = "quotes_crawl_spider"
    #logger = logging.getLogger(__name__)
    allowed_domains = ["quotes.toscrape.com"]

    start_urls = [
        "https://quotes.toscrape.com/"
    ]

    # rules is the set of 'Rule' objects that have the following properties link_extractor : LinkExtractor ; that parses the html and follows the url in the provided tag
    # follow : boolean ; this specifies if the CrawlSpider applies the same rules to the downstream pages or not
    rules = (
        Rule(
            #Link Extractor automatically knows to access the href attribte for the downflow page link
            link_extractor = LinkExtractor(
                restrict_css = "li.next a"
            ),
            callback = "parse_response",
            follow = True,
        ),
    )


    # Here we cannot override parse() function for Crawlspider because the class uses the parse function  to process the resposne with teh Rules and link followeres we configured
    # So to not interfere with that process we use a seperate function 
    def parse_response(self, response):
        self.logger.info(f"Gathering response from the page : {response.url}")
        #self.logger.info(f"Page details : {response.body}")
        #self.logger.info(BeautifulSoup(response.body,"html.parser").prettify())
        page_url = response.url

        quote_id = 0
        for quote_body in response.css("div.quote"):
            quote_text = quote_body.css("span.text::text").get()
            quote_author = quote_body.css("span small.author::text").get()
            quote_tags  = quote_body.css("div.tags a.tag::text").getall()


            # using Yield keyword makes the block of code i.e, parse_response function into a Generator
            yield {
                "page_url" : page_url,
                "quote_id" : quote_id,
                "quote_text" : quote_text,
                "quote_author" : quote_author,
                "quote_tags" : quote_tags
            }
            quote_id+=1
        

    # This is the default fucntion used to handle the source url before reaching any subsequent urls 
    # overriding this and linking it to our own "parse_response()" function will give us homogenous processingacross all the pages
    def parse_start_url(self, response):

        # yield from is acceptable from a generator block only
        # using yiled from on a simple return block will cause it to return the error : yield from self.parse_response(response); TypeError: 'NoneType' object is not iterable
        yield from self.parse_response(response)


if __name__ == "__main__":

    #logging.basicConfig(filename = "crawl_spider.log", level = logging.INFO, filemode = 'a')

    # In the settings tab the FEED handles the oubjects ommited using yield or return keywords
    # LOG_FILE handles the outputs ommited as logger.info() or logger.error()
    process = CrawlerProcess(
        settings = {
            "FEEDS" : {
                "quotes.jsonl" : {
                    "format" : "jsonlines",
                    "encoding" : "utf8",
                    "overwrite" : True
                }
            },
            "LOG_LEVEL" : "INFO",
            "LOG_FILE" : "crawl_spider.log",
            "LOG_FILE_APPEND" : True
        }
    )

    process.crawl(CrawlSpiderDemo)

    process.start()