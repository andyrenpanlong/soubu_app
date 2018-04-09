# -*- coding: utf-8 -*-
from pymongo import MongoClient
from soubu_setting import headers
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import requests
from urllib import unquote
from urllib import urlencode
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


def get_soubu_message(url, keyword, page):
    loadData = {"area_id": 0, "area_name": "", "is_hot": 0, "is_new": 0, "keyword": keyword, "label_ids": "", "page": 100,
     "parentid": 0, "price_gte": 0, "price_lte": 0, "price_order": -1, "psize": 20, "season": "", "type": 0,
     "uses_id": 0, "uses_top": 0, "vip": 0, "requestId": "", "serverId": ""}
    loadData = json.dumps(loadData)
    response = requests.post(url, data={"params": loadData}, headers=headers, verify=False)
    data_obj = json.loads(response.text)
    print data_obj["msg"]
    print data_obj["result"]
    data = data_obj["result"]["data"]


def soubu_product_list_save(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client.soubu
    db_name = "product_list"
    db[db_name].insert(data)


def soubu_devide():
    r = redis.Redis(host="127.0.0.1", port=6379, db=1)
    data = json.loads(r.lpop("soubu_message"))
    url = data["url"]
    keyword = data["keyword"]
    page = data["page"]
    print url, page, keyword
    get_soubu_message(url, keyword, page)


if __name__ == '__main__':
    soubu_devide()
