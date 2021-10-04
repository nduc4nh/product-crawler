from scrapy import Spider
import scrapy

FIELDS = {"name":"_10Wbs- _5SSWfi UjjMrh", "price":"zp9xm9 xSxKlK _1heB4J", "location":"_1w5FgK", "image":"_3-N5L6 _2GchKS"}


from selenium.webdriver import Chrome
from ..customloaders import ShopeeLoader
from ..items import ShopeeItem
import time

class ShopeeCrawler(Spider):
    DRIVER_PATH = r'drivers/chromedriver.exe'
    count = 0
    name = "shopee"
    url = r'https://shopee.vn/search?keyword='
    
    def __init__(self, name=None, **kwargs):
        super().__init__(name=name, **kwargs)
        self.name = name 
        self.start_urls = [r'https://shopee.vn/search?keyword=' + kwargs['category']]
        self.iter_stop = int(kwargs['page_num'])
        self.category = kwargs['category']
    
    def parse(self, response):
        self.count += 1
        driver = Chrome(self.DRIVER_PATH)
        driver.get(response.url)
        last_height = driver.execute_script("return document.body.scrollHeight")
        unit_height = last_height//5
        cur_height = 0
        last_width = driver.execute_script("return document.body.scrollWidth")//2
        while True:
            driver.execute_script("window.scrollTo(%d, %d);" %(last_width, cur_height))
            time.sleep(1)
            cur_height += unit_height
            if cur_height >= last_height:
                break
            driver.execute_script("window.scrollTo(0, %d);" %cur_height)
            time.sleep(1)

        res = response.replace(body = driver.page_source)
        driver.quit()

        products_name = res.xpath("//div[@class = '%s']" %FIELDS['name']).getall()
        products_price = res.xpath("//div[@class = '%s']" %FIELDS['price']).getall()
        products_location = res.xpath("//div[@class = '%s']" %FIELDS['location']).getall()
        products_image = res.xpath("//img[@class = '%s']" %FIELDS['image']).getall()

        n = len(products_price)
        print(str(len(products_image)) + "-"*30)
        for i in range(n):
            item_loader = ShopeeLoader(item=ShopeeItem(),response=res)
            item_loader.add_value("name",products_name[i])
            item_loader.add_value("price",products_price[i])
            item_loader.add_value("location",products_location[i])
            item_loader.add_value("image",products_image[i])
            item_loader._add_value("category", self.category)
            yield item_loader.load_item()
        
        
        if self.count < self.iter_stop and n != 0:
            yield scrapy.Request(self.url + "&page="+ str(self.count), callback=self.parse)
