# -*- coding: utf-8 -*-
from pymongo import MongoClient
from soubu_setting import headers
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
import json
import time
import random
import ssl
import redis
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 搜布网app数据抓取
requests = requests.Session()
ssl._create_default_https_context = ssl._create_unverified_context

headers = headers


def get_mianliao_message(page):
    print "66666666666666666666"
    time.sleep(random.randint(5, 10))
    url = "https://api.isoubu.com/sbapi/Api/Product/search_product_list"
    loadData = {"area_id": 0, "area_name": "", "is_hot": 0, "is_new": 0, "label_ids": "", "page": page, "parentid": 0,
                "price_gte": 0, "price_lte": 0, "price_order": -1, "psize": 20, "season": "", "type": 0, "uses_id": 0,
                "uses_top": 0, "vip": 0, "requestId": "", "serverId": ""}
    loadData = json.dumps(loadData)
    print "第" + str(page) + "页。。。"
    response = requests.post(url, data={"params": loadData}, headers=headers, verify=False)
    data_obj = json.loads(response.text)
    if data_obj["result"]["count"] > 0:
        print data_obj["msg"]
        print data_obj["result"]
        print data_obj["sec"]
        print data_obj["status"]
        data = data_obj["result"]["data"]
        for i in data:
            pid_only_to_redis(i["pid"])
        mianliao_product_list_save(data)


def pid_only_to_redis(pid):
    r = redis.Redis(host="127.0.0.1", port=6379, db=3)
    r.rpush("only_pid", pid)


def mianliao_product_list_save(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client.soubu
    db_name = "product_list"
    db[db_name].insert(data)


def mianliao_devide():
    r = redis.Redis(host="127.0.0.1", port=6379, db=2)
    page = json.loads(r.lpop("soubu_message_page"))
    print page
    if int(page) >= 441:
        mianliao_devide()
        return
    else:
        get_mianliao_message(page)


if __name__ == '__main__':
    mianliao_devide()
