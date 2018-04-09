# -*- coding: utf-8 -*-
from pymongo import MongoClient
import requests
import json
import time
import ssl
from urllib import urlencode
from soubu_setting import headers
import sys
reload(sys)
sys.setdefaultencoding('utf8')

# 搜布网app数据抓取
requests = requests.Session()
ssl._create_default_https_context = ssl._create_unverified_context

headers = headers


def get_soubu_message(url, keyword, page):
    keyword = keyword
    page = page or 1
    print keyword
    loadData = {"area_id": 0, "area_name": "", "is_hot": 0, "is_new": 2, "keyword": keyword, "label_ids": "", "page": 1,
                "parentid": 0, "price_gte": 0, "price_lte": 0, "price_order": -1, "psize": 20, "season": "", "type": 0,
                "uses_id": 0, "uses_top": 0, "vip": 0, "requestId": "", "serverId": ""}
    loadData = "params=" + json.dumps(loadData)
    print(loadData)
    response = requests.post(url, data=loadData, headers=headers, verify=False)
    data_obj = json.loads(response.text)
    print data_obj["msg"]
    print data_obj["result"]["count"]
    pageNum = int(data_obj["result"]["count"])/20 + 2
    for i in xrange(1, pageNum, 1):
        obj = {}
        obj["url"] = url
        obj["keyword"] = keyword
        obj["page"] = i
        print obj["url"], obj["keyword"], obj["page"]
        obj = json.dumps(obj)
        creat_redis_list(obj)

def creat_redis_list(data):
    import redis
    r = redis.Redis(host="127.0.0.1", port=6379, db=1)
    r.rpush("soubu_message", data)

if __name__ == '__main__':
    url = "https://api.isoubu.com/sbapi/Api/Product/search_product_list"
    client = MongoClient('127.0.0.1', 27017)
    db = client.soubu
    db_name = "hot_word"
    for i in list(db[db_name].find()):
        get_soubu_message(url, i["keyword"], 1)
        time.sleep(5)
