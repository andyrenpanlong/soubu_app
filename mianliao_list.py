# -*- coding: utf-8 -*-
from pymongo import MongoClient
import requests
import json
import time
from soubu_setting import headers
import random
import ssl
import redis
import sys

reload(sys)
sys.setdefaultencoding('utf8')

# 搜布网app数据抓取
requests = requests.Session()
ssl._create_default_https_context = ssl._create_unverified_context

headers = headers


def get_soubu_message(url, page):
    page = page or 1
    loadData = {"area_id": 0, "area_name": "", "is_hot": 0, "is_new": 0, "label_ids": "", "page": page, "parentid": 0,
                "price_gte": 0, "price_lte": 0, "price_order": -1, "psize": 20, "season": "", "type": 0, "uses_id": 0,
                "uses_top": 0, "vip": 0, "requestId": "", "serverId": ""}
    response = requests.post(url, data=loadData, headers=headers, verify=False)
    data_obj = json.loads(response.text)
    print data_obj["msg"]
    print data_obj["result"]
    print data_obj["sec"]
    print data_obj["status"]
    # data = data_obj["result"]["data"]
    # soubu_product_list_save(data_obj["result"]["data"])
    import redis
    r = redis.Redis(host="127.0.0.1", port=6379, db=2)

    for i in xrange(1, int(data_obj["result"]["count"])/20+2, 1):

        r.rpush("soubu_message_page", i)


def soubu_product_list_save(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client.soubu
    db_name = "product_list"
    db[db_name].insert(data)


def soubu_devide():
    url = "https://api.isoubu.com/sbapi/Api/Product/search_product_list"
    page = 1
    get_soubu_message(url, page)


if __name__ == '__main__':
    soubu_devide()
