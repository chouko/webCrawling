import datetime
import os
import re
import time
from urllib.parse import urlparse

import scrapy
from itemadapter import ItemAdapter
from scrapy.exporters import JsonItemExporter
from scrapy.pipelines.images import ImagesPipeline

from common import setting
from common.setting import ABS_PATH, DATE_TIME_PATTERN


class JsonBasePipeline:
    file_name = None

    def __init__(self):
        self.abs_path = setting.ABS_PATH
        os.makedirs(self.abs_path) if not os.path.exists(self.abs_path) else None
        self.fp = open(self.abs_path + self.file_name + '.json', "wb")
        self.exporter = JsonItemExporter(self.fp, encoding='utf-8')
        self.exporter.start_exporting()

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item

    def close_spider(self, spider):
        self.exporter.finish_exporting()
        self.fp.close()


class HtmlOutputPipeline:
    abs_path = ABS_PATH

    @classmethod
    def local2utc(cls, _time):
        if _time:
            local_st = _time
            date, times = local_st.split(' ')[0], local_st.split(' ')[1] if True else '00:00:00'
            year, month, day = int(date.split('-')[0]), int(date.split('-')[1]), int(date.split('-')[2])
            hour, minute, sec = int(times.split(':')[0]), int(times.split(':')[1]), int(times.split(':')[2])
            time_struct = time.mktime(datetime.datetime(year, month, day, hour, minute, sec, 0).timetuple())
            utc_st = datetime.datetime.utcfromtimestamp(time_struct)
            return utc_st.strftime("%Y%m%dT%H%M%SZ")

    @classmethod
    def write_html(cls, fp):
        pass

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if item["localtime"]:
            if re.match(DATE_TIME_PATTERN, item.get('localtime')):
                # 转化成utc时间
                item['localtime'] = self.local2utc(item['localtime'])
            else:
                item['localtime'] = self.local2utc(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
            path = self.abs_path + item['localtime'] + '/resource/'
            if os.path.exists(path):
                time.sleep(1)
                item['localtime'] = self.local2utc(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        path = self.abs_path + item['localtime'] + '/resource/'

        os.makedirs(path)
        fp = open(path + 'page' + '.html', "w"
                  , encoding='utf-8')
        self.write_html(fp)
        fp.close()
        return item


class ImageBasePipeline(ImagesPipeline):
    abs_path = ABS_PATH

    def get_media_requests(self, item, info):
        adapter = ItemAdapter(item)
        for image_url in adapter['image_urls']:
            yield scrapy.Request(image_url)

    def file_path(self, request, response=None, info=None, *, item=None):
        return self.abs_path + urlparse(request.url).path
