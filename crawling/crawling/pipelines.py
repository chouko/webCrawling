# Define your item pipelines here

# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import os
import time
import datetime
from os.path import dirname, abspath
from urllib.parse import urlparse

import scrapy
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
from scrapy.exporters import JsonItemExporter

from items import JsonOutputsSingleItem

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
        if adapter.get('localtime') is not None:
            # 转化成utc时间
            adapter['localtime'] = local2utc(adapter['localtime'])
        else:
            adapter['localtime'] = local2utc(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        self.mkdir(self.abs_path + adapter['localtime'] + '/resource')
        return item

    def mkdir(self, path):
        if not os.path.exists(path):
            os.makedirs(path)
        else:
            os.makedirs(self.abs_path + time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()) + '/resource')


# json文件导出管道
class JsonOutputPipeline:

    def __init__(self):
        self.abs_path = ABS_PATH
        os.makedirs(self.abs_path) if not os.path.exists(self.abs_path)
        self.fp = open(self.abs_path + 'res-list.json', "wb")
        self.exporter = JsonItemExporter(self.fp, encoding='utf-8')
        self.exporter.start_exporting()

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

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()


# html文件导出管道
class ResourceOutputPipeline:
    abs_path = ABS_PATH

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        fp = open(self.abs_path + adapter['localtime'] + '/resource/' + 'page' + '.html', "w"
                  , encoding='utf-8')
        fp.write(message % (adapter['body']))
        fp.close()
        return item


def local2utc(local_st):
    date, times = local_st.split(' ')[0], local_st.split(' ')[1]
    year, month, day = int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2])
    hour, minute, sec = int(times.split(':')[0]), int(times.split(':')[1]), int(times.split(':')[2])
    time_struct = time.mktime(datetime.datetime(year, month, day, hour, minute, sec, 0).timetuple())
    utc_st = datetime.datetime.utcfromtimestamp(time_struct)
    return utc_st.strftime("%Y%m%dT%H%M%SZ")
