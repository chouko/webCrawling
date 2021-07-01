import json
import time
from json import JSONDecodeError

from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib import parse

import setting


class ListSearch:
    __driver = webdriver.Chrome(setting.ABS_PATH + '/chromedriver/chromedriver.exe')
    __driver.get(setting.WECHAT_LOGIN)
    __driver.implicitly_wait(15)  # 手动扫描二维码
    __driver.find_element(By.XPATH, '//ul[@class="weui-desktop-sub-menu"]/li[1]/a').click()
    __params = parse.parse_qs(parse.urlparse(__driver.current_url).query)

    @property
    def params(self):
        return self.__params

    @staticmethod
    def fetch_list(url):
        ListSearch.__driver.get(url)
        try:
            obj = json.loads(ListSearch.__driver.find_element(By.TAG_NAME, 'pre').text)
        except ValueError:
            return None
        except TypeError:
            return None
        if obj['base_resp']['ret'] == 200013:
            print("频繁了, 开始sleep………………")
            time.sleep(7200)
            print("重新开爬………………")
        if len(obj['app_msg_list']) == 0:
            print("爬完了")
        return ListSearch.__driver.page_source
