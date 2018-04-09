# -*- coding: utf-8 -*-
import redis
from pymongo import MongoClient
import time
import sys
reload(sys)
sys.setdefaultencoding('utf8')

client = MongoClient('127.0.0.1', 27017)
# 连接所需数据库, sf_fy（一起做网店）为数据库名称
db = client.soubu

def zhengli():
    product_list = list(db["product_info"].find())
    for i in xrange(0, len(product_list), 1):
        data = product_list[i]["data"]
        print "插入数据", data
        data_unique(data)
    print "数据整理完毕，继续监控执行..."
    time.sleep(60*1800) # 每隔半小时整理一次数据
    zhengli()

def data_unique(data):
    unique_data = int(data["pid"])
    product_list_id = len(list(db["product_info"].find({"pid": unique_data})))
    if product_list_id < 1:
        db["product_info_unique"].insert(data)


zhengli()