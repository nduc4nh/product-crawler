from itemloaders import flatten
from itemloaders.processors import Join, MapCompose, TakeFirst
from scrapy.loader import ItemLoader
import re


#This is where we define a custom ItemLoaders
#ItemLoaders are Wrapper Object which help to validate data before putting them into an Item Object
from bs4 import BeautifulSoup

def validate_name(x):
    x = flatten(x)
    tmp = TakeFirst()(x)
    bs = BeautifulSoup(tmp)
    re = "#".join([ele.text for ele in bs.find_all('div')])
    return re.strip()

def validate_location(x):
    x = flatten(x)
    tmp = TakeFirst()(x)
    bs = BeautifulSoup(tmp)
    re = "#".join([ele.text for ele in bs.find_all('div')])
    return re.strip()

def validate_price(x):
    x = flatten(x)
    tmp = TakeFirst()(x)
    bs = BeautifulSoup(tmp)
    re = "-".join([ele.text for ele in bs.find_all(attrs={'class':'_1d9_77'})]) #id of class indicating money
    return re

def validate_image(x):
    x = flatten(x)
    tmp = TakeFirst()(x)
    try:
        bs = BeautifulSoup(tmp)
        re = bs.find("img").attrs['src']
    except:
        re = ""
    return re.strip()


class ShopeeLoader(ItemLoader):
    default_output_processor = TakeFirst()
    price_in = validate_price
    name_in = validate_name 
    location_in = validate_location
    image_in = validate_image