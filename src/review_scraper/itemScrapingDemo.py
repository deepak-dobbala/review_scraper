import datetime
import pathlib

import scrapy
from scrapy.crawler import CrawlerProcess
from itemModels.QuoteModel import QuoteModelItem, QuoteModelDataclass

class itemScrapingDemo(scrapy.Spider):
    name = "itemScrapingDemo"

    async def start(self):
        start_urls = [ "https://quotes.toscrape.com/",]

        for start_url in start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse, meta={"page_id":0, "stat_time" : datetime.datetime.now().isoformat()})

    def parse(self, response):
        page_id = response.meta["page_id"]
        response.meta["url"] = str(response)
        quote_id = -1
        yield response.meta
        data = []
        for quote in response.css("div.quote"):
            quote_text = quote.css("span.text::text").get()
            quote_author = quote.css("small.author::text").get()
            quote_tags = quote.css("div.tags a.tag::text").getall()
            quote_id+=1   
            
            # yield {
            #     "page_ID" : page_id,
            #     "quote_ID" : quote_id,
            #     "quote_text" : quote_text,
            #     "quote_author" : quote_author,
            #     "quote_tags" : quote_tags,
            # }
            quote_obj = QuoteModelDataclass(quote_text = quote_text, quote_author = quote_author, quote_tags = quote_tags, page_index=str(page_id))
            yield quote_obj

        next_page_list = response.css("li.next a[href^='/page']::attr(href)").getall()
        yield from response.follow_all(next_page_list, callback = self.parse, meta = {"page_id":page_id+1, "start_time":datetime.datetime.now().isoformat()})

if __name__ == "__main__":
    crawler = CrawlerProcess(
        settings={ 
            "FEEDS":{
                "quotes.jsonl":{
                    "format" : "jsonlines",
                    "encoding" : "utf8",
                    "overwrite" : True,
                }
            },
            "LOG_FILE" : "crawl_spider.log",
            "LOG_LEVEL" : "INFO",
            "LOG_FILE_APPEND" : True,
        }
    )

    crawler.crawl(itemScrapingDemo)

    crawler.start()