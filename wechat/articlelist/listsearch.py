import json
import time
from random import randint

from selenium import webdriver
from selenium.webdriver.common.by import By
from urllib import parse

from setting import WECHAT_LOGIN, WHCHAT_LIST_FORMAT

from common.setting import ABS_PATH


class ListSearch:
    __driver = webdriver.Chrome(ABS_PATH + '/chromedriver/chromedriver.exe')

    def fetch_list(self):
        driver = ListSearch.__driver
        driver.get(WECHAT_LOGIN)
        driver.implicitly_wait(15)  # 手动扫描二维码
        driver.find_element(By.XPATH, '//ul[@class="weui-desktop-sub-menu"]/li[1]/a').click()
        link = driver.current_url
        params = parse.parse_qs(parse.urlparse(link).query)
        i = 0
        res = {"res": []}
        while True:
            url = WHCHAT_LIST_FORMAT.format(i, params["token"][0])
            driver.get(url)
            obj = json.loads(driver.find_element(By.TAG_NAME, 'pre').text)
            print("url: " + url)
            if obj['base_resp']['ret'] == 200013:  # 频繁了
                print("频繁了")
                break
            if len(obj['app_msg_list']) == 0:
                print("爬完了")
                break
            res["res"].append(obj['app_msg_list'])
            i += 5
            time.sleep(randint(30, 50))

        with open(ABS_PATH + "/record.json", "w") as f:
            json.dump(res, f)
