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


def get_length():
    print len(list(db["product_list"].find().distinct('pid')))
    for i in list(db["product_list"].find().distinct('pid')):
        for j in list(db["product_info"].find()):
            if j["data"]["pid"] != i:
                print i

def dain():
    print len(list(db["shop_info_mess"].find().distinct('公司名称')))
    # for i in list(db[db_name].find()):
    #     print i["data"]["pid"]


dain()