# Define your item pipelines here

# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import re
import time
import datetime
from os.path import dirname, abspath
from urllib.parse import urlparse

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonLinesItemExporter

ABS_PATH = dirname(dirname(abspath(__file__))) + '/news/'
fields_to_export = ['title', 'category', 'summary']
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
class MyImagesPipeline(ImagesPipeline):
    abs_path = ABS_PATH

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        for image_url in adapter['image_urls']:
            yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        adapter = ItemAdapter(item)
        return self.abs_path + adapter['localtime'] + '/' + os.path.basename(urlparse(request.url).path)


# 文件夹创建管道
class DirCreatingPipeline:
    abs_path = ABS_PATH

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if adapter.get('localtime'):
            # 转化成utc时间
            adapter['localtime'] = local2utc(adapter['localtime'])
        else:
            adapter['localtime'] = adapter['title']
        mkdir(self.abs_path + adapter['localtime'] + '/resource')
        return item


# json文件导出管道
class JsonOutputPipeline:
    abs_path = ABS_PATH

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fp = open(self.abs_path + adapter['localtime'] + '/' + 'dto.json', "wb")
        exporter = JsonLinesItemExporter(fp, encoding='utf-8', fields_to_export=fields_to_export)
        exporter.export_item(item)
        fp.close()
        return item


# html文件导出管道
class ResourceOutputPipeline:
    abs_path = ABS_PATH

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fp = open(self.abs_path + adapter['localtime'] + '/resource/' + adapter['title'] + '.html', "w"
                  , encoding='utf-8')
        fp.write(message % (adapter['body']))
        fp.close()
        return item


def mkdir(path):
    if not os.path.exists(path):
        os.makedirs(path)


def local2utc(local_st):
    date, times = local_st.split(' ')[0], local_st.split(' ')[1]
    year, month, day = int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2])
    hour, minute, sec = int(times.split(':')[0]), int(times.split(':')[1]), int(times.split(':')[2])
    time_struct = time.mktime(datetime.datetime(year, month, day, hour, minute, sec, 0).timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st.strftime("%Y%m%dT%H%M%SZ")
