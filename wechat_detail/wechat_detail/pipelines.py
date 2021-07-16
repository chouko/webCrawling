import datetime
import os
import time
from urllib.parse import urlparse

from itemadapter import ItemAdapter

from common.items import JsonOutputsSingleItem
from common.pipelines.base_pipelines import JsonBasePipeline, ImageBasePipeline
from common.setting import ABS_PATH


class WechatDetailHtmlOutputPipeline:
    abs_path = ABS_PATH + '/wechat_detail_news/'

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        if type(adapter["timestamp"]) is int:
            # 转化成utc时间
            item['timestamp'] = local2utc(item['timestamp'])
        else:
            item['timestamp'] = local2utc(int(time.time()))
        path = self.abs_path + item['timestamp'] + '/resource/'
        if os.path.exists(path):
            time.sleep(1)
            item['timestamp'] = local2utc(int(time.time()))
        path = self.abs_path + item['timestamp'] + '/resource/'

        os.makedirs(path)
        fp = open(path + 'page' + '.html', "w"
                  , encoding='utf-8')
        fp.write(adapter['html'])
        fp.close()
        return item


class JsonOutputPipeline(JsonBasePipeline):
    file_name = '/wechat_detail_news'

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        new_item = JsonOutputsSingleItem()
        new_item['path'] = adapter['timestamp']
        new_item['title'] = adapter['title']
        new_item['category'] = adapter['category']
        new_item['tag'] = ['OTHER']
        new_item['summary'] = adapter['summary']
        self.exporter.export_item(new_item)
        return item


class WechatImgPipeline(ImageBasePipeline):
    abs_path = ABS_PATH

    def file_path(self, request, response=None, info=None, *, item=None):
        query = urlparse(request.url).query
        if query is not None:
            prefix = query.split('=')[-1]
            return self.abs_path + urlparse(request.url).path + '.' + prefix
        return self.abs_path + urlparse(request.url).path


def local2utc(local_st):
    date_array = datetime.datetime.utcfromtimestamp(local_st)
    utc_time = date_array.strftime("%Y%m%dT%H%M%SZ")
    return utc_time
