import json
import os
from functools import reduce
from operator import add

from common.setting import ABS_PATH


class JsonFileInput(object):
    def __init__(self, dir_name):
        self.dir_name = ABS_PATH + '/' + dir_name + '/'

    def input_result(self):
        result = []
        for file_name in os.listdir(self.dir_name):
            with open(ABS_PATH + '/' + 'list-res' + '/' + file_name, 'r', encoding='utf8') as fp:
                json_data = list(json.loads(fp.read()))
                result.extend(reduce(add, list(map(lambda item: item.get("app_msg_list"), json_data))))
        return result


