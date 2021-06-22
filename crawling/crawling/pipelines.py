# Define your item pipelines here

# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time
import datetime
from os.path import dirname, abspath

import scrapy
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline


# 执行顺序参考settings.ITEM_PIPELINES
class ImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        for image_url in adapter['images']:
            yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        return DirCreatingPipeline.abs_path + '/news' + adapter['localtime']


class DirCreatingPipeline:
    abs_path = dirname(dirname(abspath(__file__)))

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('localtime'):
            # 转化成utc时间
            adapter['localtime'] = local2utc(adapter['localtime'])
        else:
            adapter['localtime'] = adapter['title']
        mkdir(self.abs_path + '/news' + adapter['localtime'] + 'resource')


def mkdir(path):
    if not os.path.exists(path):  # 判断是否存在文件夹如果不存在则创建为文件夹
        os.makedirs(path)


def local2utc(local_st):
    date, times = local_st.split(' ')[0], local_st.split(' ')[1]
    year, month, day = date.split('-')[0], date.split('-')[1], date.split('-')[2]
    hour, minute, sec = times.split(':')[0], times.split(':')[1], times.split(':')[2]
    time_struct = time.mktime(datetime.datetime(year, month, day, hour, minute, sec, 0).timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st.strftime("%Y%m%dT%H%M%SZ")
