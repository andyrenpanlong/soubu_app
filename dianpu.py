# -*- coding: utf-8 -*-
from pymongo import MongoClient
import requests
import json
import time
import redis
import ssl
from urllib import urlencode
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from soubu_setting import headers
import random
import sys
reload(sys)
sys.setdefaultencoding('utf8')
sys.setrecursionlimit(1000000)
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 搜布网app数据抓取
requests = requests.Session()
ssl._create_default_https_context = ssl._create_unverified_context

headers = headers

def get_soubu_dianpu_message(url, pid):
    loadData = {"business": 0, "from_type": 0, "from_user": 0, "is_filter": 3, "pid": pid, "scene": 31, "type": 0,
                "requestId": ""}
    loadData = "params=" + json.dumps(loadData)
    response = requests.post(url, data=loadData, headers=headers, verify=False)
    data_obj = json.loads(response.text)
    print data_obj
    data = data_obj["result"]
    print data
    if data == {} or data == "{}":
        shop_devide()
    else:
        user_id = data["data"]["user_id"]
        get_shop_info(user_id)
        dianpu_message_save(data)

def get_shop_info(user_id):
    url = "https://api.isoubu.com/sbapi/Api/Shop/get_shop_info"
    loadData = {"user_id": user_id, "requestId": "15204229317381653751420", "serverId": ""}
    loadData = "params=" + json.dumps(loadData)
    response = requests.post(url, data=loadData, headers=headers, verify=False)
    data_obj = json.loads(response.text)
    data = data_obj["result"]
    if data == {} or data == "{}":
        shop_devide()
    else:
        shop_info_save(data)
        print data

def shop_info_save(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client.soubu
    db_name = "shop_info"
    db[db_name].insert(data)

def dianpu_message_save(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client.soubu
    db_name = "product_info"
    db[db_name].insert(data)

def shop_devide():
    url = "https://api.isoubu.com/sbapi/Api/Product/product_info"
    r = redis.Redis(host="127.0.0.1", port=6379, db=3)
    pid = json.loads(r.lpop("only_pid"))
    get_soubu_dianpu_message(url, pid)
    time.sleep(random.randint(5, 10))
    shop_devide()

if __name__ == '__main__':
    shop_devide()
