import getopt
import sys

argvs = sys.argv[1:]

opt, arg = getopt.getopt(argvs,"t:c:h",["category","page_num","help"])
category = None
page_num = 1

from scrapy.crawler import CrawlerProcess
from shopee.shopee.spiders.shopee import ShopeeCrawler
manual = """
    -t: the type of product
    -c: number of pages to crawl
"""

reminder = """
product_crawler.py --help for detail reference

product_crawler.py --t=<category name> --c=<page_num>"""

err = False
try: 
    for arg,val in opt:
        if arg in  ("-t"):
            print(val)
            if val:
                category = val
            else:
                err = True
        elif arg in ("-c"):
            if val:
                page_num = val
            else:
                err = True
                
        elif arg in ("-h","--help"):
            print(manual)

    if (not category) or err:
        print(reminder)
    else:
        proc = CrawlerProcess()
        proc.crawl(ShopeeCrawler,'shopee', category = category, page_num = page_num)
        proc.start()
except:
    print(reminder)

