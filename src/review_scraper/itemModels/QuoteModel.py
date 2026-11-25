# Item Declaration  is used to defin eth schema which is used to hold the data being scraped from the spiders
# the objects that are getting scraped must be supported by itemloader which will only then allow the data to enter the itempipelines for processing

# Method 1 : using the native scrapy Field methods it stores the data as dict based key - value pairs
import scrapy

class QuoteModelItem(scrapy.Item):
    quote_text = scrapy.Field()
    quote_author = scrapy.Field()
    quote_tags = scrapy.Field()

    
# Method 2 : using dataclasses for better type hints, these are only type hints they are not enforced during runtime
from dataclasses import dataclass

@dataclass
class QuoteModelDataclass():
    quote_text : str
    quote_author : str
    quote_tags : list[str]
    page_index : int

# Method 2 : attrs library is a py package that modularizes the approach of riting  classes and accesing data from the class objects 
# attrs module decentralizes  the creation of dunder methods i.e, __init__, __eq__ etc
import attrs

@attrs.define
class QuoteModelAttrs():
    quote_text = attrs.field()

