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
    product_list_num = len(list(db["product_list"].find().distinct('pid')))
    product_info_num = len(list(db["product_info"].find()))
    shop_info_num = len(list(db["shop_info"].find()))
    print "product_list_num：", product_list_num
    print "product_info_num：", product_info_num
    print "shop_info_num：", shop_info_num
    print "\n"
    time.sleep(60)
    get_length()

get_length()