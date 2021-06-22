# -*- coding: utf-8 -*-
import time
import datetime
from os.path import dirname, abspath


# from scrapy import cmdline
# if __name__ == '__main__':
#     cmdline.execute("scrapy crawl crawling".split())
def local2utc(local_st):
    time_struct = time.mktime(local_st.timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st.strftime("%Y%m%dT%H%M%SZ")


if __name__ == '__main__':
    print(local2utc(datetime.datetime(2014, 9, 18, 10, 42, 16)))
