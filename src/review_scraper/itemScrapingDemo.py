import datetime
import pathlib

import scrapy
from scrapy.crawler import CrawlerProcess
from itemModels.QuoteModel import QuoteModelItem, QuoteModelDataclass, QuoteModelAttrs
from itemModels.AuthorModel import AuthorModelItem

class itemScrapingDemo(scrapy.Spider):
    name = "itemScrapingDemo"

    async def start(self):
        start_urls = [ "https://quotes.toscrape.com/",]

        for start_url in start_urls:
            yield scrapy.Request(url=start_url, callback=self.parse, meta={"page_id":0, "stat_time" : datetime.datetime.now().isoformat()})

    def parse_author(self, response):
        author_name = response.css("div.author-details h3.author-title::text").get()
        author_dob = response.css("div.author-details p span.author-born-date::text").get()
        author_desc = response.css("div.author-details div.author-description::text").get()

        try : 
            yield AuthorModelItem(author_name = author_name, author_dob = author_dob, author_desc = author_desc)
        except ValueError as valErr:
            self.logger.error(f"AuthorModelItem : Value mismatch : {valErr}")
        except Exception as exp:
            self.logger.error(f"AuthorModelItem : Exception occured : {exp}")

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
            try:
                quote_obj = QuoteModelAttrs(quote_text = quote_text, quote_author = quote_author, quote_tags = quote_tags, page_index=page_id)
                yield quote_obj
            except ValueError as valErr:
                self.logger.error(f"QuoteModelItem : page_id : {page_id} is invalid raised an value error : {valErr}")
            except TypeError as typeErr:
                self.logger.error(f"QuoteModelItem : Invalid type received : {typeErr}")
            except Exception as exp:
                self.logger.error(f"QouteModelItem : Exception occured : {exp}")
            

        next_page_list = response.css("li.next a[href^='/page']::attr(href)").getall()
        yield from response.follow_all(next_page_list, callback = self.parse, meta = {"page_id":page_id+1, "start_time":datetime.datetime.now().isoformat()})

        author_page_list = response.css("div.quote span a[href^='/author']::attr(href)").getall()
        yield from response.follow_all(author_page_list, callback = self.parse_author, meta={"scrape_time":datetime.datetime.now().isoformat()})

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