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
# 禁用安全请求警告
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# 搜布网app数据抓取
requests = requests.Session()
ssl._create_default_https_context = ssl._create_unverified_context

headers = headers


def product_list_only():
    r = redis.Redis(host="127.0.0.1", port=6379, db=3)
    client = MongoClient('127.0.0.1', 27017)
    db = client.soubu
    db_name = "product_list_2"
    for pid in db[db_name].find():
        # print pid["pid"]
        r.rpush("only_pid", pid["pid"])

if __name__ == '__main__':
    product_list_only()
