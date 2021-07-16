# Define your item pipelines here

# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
import time
import datetime
from urllib.parse import urlparse

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.files import FilesPipeline
from scrapy.pipelines.images import ImagesPipeline

from common.items import JsonOutputsSingleItem
from common.pipelines import base_pipelines
from crawling.constant_settings import ABS_PATH, DOMAIN

from common.pipelines.base_pipelines import ImageBasePipeline
from common.setting import DATE_TIME_PATTERN

message = """
<html>
<head>
<body>
%s
</body>
</head>
</html>"""


# 执行顺序参考settings.ITEM_PIPELINES
# 详细页面的图像获取管道
class MyImagesPipeline(ImageBasePipeline):
    abs_path = ABS_PATH


# json文件导出管道
class JsonOutputPipeline(base_pipelines.JsonBasePipeline):
    file_name = '/res-list'

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        new_item = JsonOutputsSingleItem()
        new_item['path'] = adapter['localtime']
        new_item['title'] = adapter['title']
        new_item['category'] = adapter['category']
        new_item['tag'] = []
        new_item['summary'] = adapter['summary']
        self.exporter.export_item(new_item)
        return item


# html文件导出管道
class ResourceOutputPipeline:
    abs_path = ABS_PATH

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if item.get('localtime') is not None and re.match(DATE_TIME_PATTERN, item.get('localtime')):
            # 转化成utc时间
            item['localtime'] = local2utc(item['localtime'])
        else:
            item['localtime'] = local2utc(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        path = self.abs_path + item['localtime'] + '/resource/'
        if os.path.exists(path):
            time.sleep(1)
            item['localtime'] = local2utc(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        path = self.abs_path + item['localtime'] + '/resource/'

        os.makedirs(path)
        fp = open(path + 'page' + '.html', "w"
                  , encoding='utf-8')
        fp.write(message % (adapter['body']))
        fp.close()
        return item


# 其他文件导出管道
class SourceFilePipeline(FilesPipeline):
    abs_path = ABS_PATH

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        for url in adapter['resource_links']:
            yield scrapy.Request(DOMAIN + url)

    def file_path(self, request, response=None, info=None, *, item=None):
        return self.abs_path + '/' + urlparse(request.url).path


def local2utc(local_st):
    date, times = local_st.split(' ')[0], local_st.split(' ')[1] if True else '00:00:00'
    year, month, day = int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2])
    hour, minute, sec = int(times.split(':')[0]), int(times.split(':')[1]), int(times.split(':')[2])
    time_struct = time.mktime(datetime.datetime(year, month, day, hour, minute, sec, 0).timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st.strftime("%Y%m%dT%H%M%SZ")
