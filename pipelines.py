# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
import time

from common.pipelines import base_pipelines


class WechatPipeline(base_pipelines.JsonBasePipeline):
    file_name = '/' + time.strftime("%Y%m%d%H%M%S", time.localtime())
