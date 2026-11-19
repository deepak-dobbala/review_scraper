import sys
# Scrapy is for fast and reliable multi threaded crawling framework that uses HTTP responses to collect information
import scrapy
# BeautifulSoup or bs4 is for theformatting and linting sections of the response  body; can also be used for parsing and modifying the data in the HTML or XMl data
from bs4 import BeautifulSoup
from pathlib import Path
import datetime

from scrapy.crawler import CrawlerProcess

# to run the spider wee have two ways 
# 1. use crawl > $ scrapy crawl quotes , this willwork when  the scrapy rpoejct was initalized
# 2. use runspider > $ scrapy runspider main.py , this works for standalone files that can be runin regular python projects
# the second cmd also includes an --output flaga or -o flag i.e, $ scrapy runspider main.py -o file.jsonl

# we can use an output.json or output.jsonl the only difference is that json stores data as an array of jsonn objects 
# meanwhile jsonl stores the json objects each in a new line seperated by '/n' character
class DemoScraper(scrapy.Spider):
    name="quotes"

    async def start(self):
        # Scrapy hits these url when started with the cmd $scrapy runspider main.py -o output.jsonl [The output flags ]
        start_urls=[
            "https://quotes.toscrape.com/",
            #"https://quotes.toscrape.com/page/2",
        ]

        # SCrapy does not  use threads instead  of which it sends out async await requests and it does not waste any computing potential on watiting for the ressponse
        index=0
        for url in start_urls:
            # Insert th page_id into the metadata which will beused to bookmark the responses 
            yield scrapy.Request(url=url, callback=self.parse, meta={"page_id":index, "time":datetime.datetime.now().isoformat()})
            index+=1

    def parse(self, response):

        # The following set of commented lines of code is to see the html data before performing any processing on the data it automatically formats and pushes the data into a file

        # page_id = response.meta['page_id']
        # file_path = Path(f"pages/Quotes-{page_id}.html")
        # # This line make sure the parents of the targeted file_patth exists so that the open() function doesnot throuw an error
        # file_path.parent.mkdir(parents=True, exist_ok=True)
        # # The function prettify() parses the response body to print it in a formatted version
        # html_soup = BeautifulSoup(response.body,'html.parser')
        # with open(file_path,'w') as output_file:
        #     output_file.write(html_soup.prettify())
        #print(f"written to the file {file_path}") 
        page_id = response.meta['page_id']
        response.meta["url"] = str(response)
        quote_id = 0
        yield response.meta
        file_path = Path(f"pages/Quotes-page-{response.meta["page_id"]}.jsonl")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        data = []
        for quote in response.css("div.quote"):
            quote_text = quote.css("span.text::text").get()
            quote_author = quote.css("small.author::text").get()
            quote_tags = quote.css("div.tags a.tag::text").getall()
            quote_id+=1
            # print(
            #     dict( text = quote_text, author=quote_author, tags = quote_tags)
            # )   
            
            yield {
                "page_ID" : page_id,
                "quote_ID" : quote_id,
                "quote_text" : quote_text,
                "quote_author" : quote_author,
                "quote_tags" : quote_tags,
            }
        # with open(file_path,'w') as output_file:
        #     for record in data:
        #         output_file.write(str(record)+"\n")

        # we can use Two type of fcallback functions to trigger the link following on is the usual scrapy.Request() fucntions  which returns a callback function that will access the info from the reroute url
        # The second Method is using response.follow() function  it will also return a request object but is not required to urljoin() before hand
        # we can also use a follow_all() function to throw in all the next__page linkes without having to loop over the list
        # in the Request objects for scrapy the 'callback' attribute dictates what function should be executed once the HTML resposneis obtained

        for next_page in response.css('li.next a[href^="/page"]::attr(href)').getall():
            if next_page is None:
                continue
            yield response.follow(next_page,callback = self.parse, meta = {"page_id":page_id+1})

        next_page_list = response.css("li.next a[href^='/page']::attr(href)").getall()
        yield from response.follow_all(next_page_list, callback = self.parse, meta = {"page_id":page_id+1})

        next_page = response.css('li.next a[href^="/page"]::attr(href)').get()
        next_page = response.urljoin(next_page)
        yield scrapy.Request(next_page, callback = self.parse, meta = {"page_id":page_id+1})


# WE usually donot run multiple scrapers if we want tohave a standalone file we need to segregate  the files for specifc scraping purpose

class DemoScraper2(scrapy.Spider):
    name = "quotes2"

    async def start(self):
        index=2
        start_urls = [
            "https://quotes.toscrape.com/page/2"
        ]
        for url in start_urls:
            yield scrapy.Request(url = url, callback = self.parse, meta = {"page_id":index, "time": datetime.datetime.now().isoformat()})
            index+=1

    def parse(self, response):
        yield response.meta
        page_id = response.meta["page_id"]    
        quote_id = 0
        for quote in response.css("div.quote"):
            quote_text = quote.css("span.text::text").get()
            quote_author = quote.css("small.author::text").get()
            quote_tags = quote.css("div.tags a.tag::text").getall()
            quote_id+=1

            yield {
                "page_id" : page_id,
                "quote_id" : quote_id,
                "quote_text" : quote_text,
                "quote_author" :quote_author,
                "quote_tags" : quote_tags,
            }
        

if __name__=="__main__":
    crawler = CrawlerProcess(
        settings= {
            "FEEDS": {
                "quotes.jsonl": {
                    "format" : "jsonlines",
                    "encoding" : "utf8",
                    "overwrite" : False,
                }
            }
        }
    )

    #crawler.crawl(DemoScraper2)
    crawler.crawl(DemoScraper)

    crawler.start()