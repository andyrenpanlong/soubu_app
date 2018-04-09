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
sys.setrecursionlimit(100000000)
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
    data = data_obj["result"]
    print "345435", data_obj
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
    data = data_obj["result"]["data"]
    print data
    if data == {} or data == "{}":
        shop_devide()
    else:
        # shop_info_save(obj)
        obj = {}
        obj["名称"] = data["name"]
        obj["公司名称"] = data["company"]
        obj["主营行业"] = data["main_industry"]
        obj["主营产品"] = data["main_product"]
        obj["联系电话"] = data["phone"]
        obj["公司地址"] = data["detail_address"]
        obj["公司简介"] = data["company_profile"]
        obj["联系人"] = data["contact_name"]
        data2 = get_evaluation(user_id, obj)
        shop_info_save(data2)
        print data


# 获取商铺评价信息
def get_evaluation(user_id, obj):
    obj = obj
    url = "https://api.isoubu.com/sbapi/Api/OrderEvaluation/get_shop_evaluation"
    loadData = {"page": 1, "psize": 21, "user_id": user_id, "requestId": "1521009342883460162423", "serverId": ""}
    loadData = "params=" + json.dumps(loadData)
    response = requests.post(url, data=loadData, headers=headers, verify=False)
    data_obj = json.loads(response.text)
    data = data_obj["result"]
    obj["累计交易"] = data["order_count"]
    obj["全部评价"] = data["count"]
    return obj


def shop_info_save(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client.soubu
    db_name = "shop_info_mess"
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
    # pid = 105048
    get_soubu_dianpu_message(url, pid)
    time.sleep(random.randint(5, 12))
    shop_devide()


if __name__ == '__main__':
    shop_devide()
