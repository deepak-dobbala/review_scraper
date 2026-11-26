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

# Method 3 : attrs library is a py package that modularizes the approach of riting  classes and accesing data from the class objects 
# attrs module decentralizes  the creation of dunder methods i.e, __init__, __eq__ etc, and is best suited for DTO [Data Transfer Objects]
import attrs

# This is a validation function to check the values entering the attributes
def validate_page_id(instance, attribute, value):
    if value<0:
        raise ValueError("Page_id cannot be negative")

# define() decorator is used to create the dunder functions duch as __init__ , __eq__ etc using the attributes provided and the default values
@attrs.define
class QuoteModelAttrs():
    # the field() function is used to decalre the attribute : type defines the metadaata this doe ssnot enforce any type safely it is purely for metadata purposes
    # converter is sthe attribute that enforces type safety takes in the Callable object such as int or str.split it is converted to int(value) or str.split(value)
    # validator enforces data constraints and the default values represents the default value of the attribute is nothing was assigned
    quote_text = attrs.field(type = str)
    quote_author = attrs.field(type = str)
    quote_tags = attrs.field(type = list[str], default=[])
    page_index = attrs.field(type = int, converter = int, validator=validate_page_id, default=0)



# Method 4 :  we can use Pydantic for extra type safe classes but the validation on pydantic is a lot slower compared to atts module 
# Pydnantic also has more memory footprint whihc make it bloated for larger data  blocka whihc is 30-40* the memory consumed by attrs
# attrs uses native c pointers to manage dat awhere as pydnatic uses rust to maange and validate the data 