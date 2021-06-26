# -*- coding: utf-8 -*-
from scrapy import cmdline
if __name__ == '__main__':
    cmdline.execute("scrapy crawl news_list_detail".split())
    # cmdline.execute("scrapy crawl news_detail".split())

