from scrapy.utils.project import get_project_settings
from shopee.shopee.spiders.shopee import ShopeeCrawler
from scrapy.crawler import CrawlerProcess
import getopt
import sys

argvs = sys.argv[1:]

opt, arg = getopt.getopt(argvs, "t:c:l:h", ["category", "page_num", "help"])
category = None
location = None
page_num = 1


manual = """
    -t: the type of product
    -c: number of pages to crawl
    -l: location: mongodb || ibmcloudant
"""

reminder = """
product_crawler.py --help for detail reference

product_crawler.py --t=<category name> --c=<page_num> -l=[mongodb||ibmcloudant]"""

err = False
try:
    for arg, val in opt:
        if arg in ("-t"):
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
        elif arg in ("-l"):
            if val:
                location = val
            else:
                err = True

        elif arg in ("-h", "--help"):
            print(manual)

    if (not category) or (not location) or err:
        print(reminder)
    else:
        settings = get_project_settings()
        if location == "mongodb":
            settings.set("MONGO_URI", "mongodb+srv://anhnd:Dota2fan@cluster0.3myha.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            settings.set("MONGO_DATABASE", "products")
            settings.set("ITEM_PIPELINES", {
                         'shopee.shopee.pipelines.MongoShopeePipeline': 300})
        elif location == "ibmcloudant":
            settings.set("BROKERS",
                         ["broker-0-0drdc86t23zxnbkj.kafka.svc08.us-south.eventstreams.cloud.ibm.com:9093",
                          "broker-4-0drdc86t23zxnbkj.kafka.svc08.us-south.eventstreams.cloud.ibm.com:9093",
                          "broker-3-0drdc86t23zxnbkj.kafka.svc08.us-south.eventstreams.cloud.ibm.com:9093",
                          "broker-2-0drdc86t23zxnbkj.kafka.svc08.us-south.eventstreams.cloud.ibm.com:9093",
                          "broker-1-0drdc86t23zxnbkj.kafka.svc08.us-south.eventstreams.cloud.ibm.com:9093",
                          "broker-5-0drdc86t23zxnbkj.kafka.svc08.us-south.eventstreams.cloud.ibm.com:9093"])

        proc = CrawlerProcess(settings)
        proc.crawl(ShopeeCrawler, 'shopee',
                   category=category, page_num=page_num)
        proc.start()


except:
    print(reminder)
