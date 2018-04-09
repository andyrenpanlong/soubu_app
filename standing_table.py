# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
import json
import urllib
import tsv
import sys
reload(sys)
sys.setdefaultencoding('utf8')

client = MongoClient('127.0.0.1', 27017)
db = client.soubu

# 导出店铺信息
def standing_tables():
    db_name = "shop_info_2"
    # table_lists = []
    for i in list(db[db_name].find()):
        data = i
        obj = {}
        obj["公司名称"] = data["company"]
        obj["主营行业"] = data["main_industry"]
        obj["主营产品"] = data["main_product"]
        obj["联系电话"] = data["phone"]
        obj["公司地址"] = data["detail_address"]
        obj["公司简介"] = data["company_profile"]
        obj["联系人"] = data["contact_name"]
        # table_lists.append(obj)
        data_list = list(db["shop_info_message_2"].find({"公司名称": obj["公司名称"]}))
        # print data
        if len(data_list) < 1:
            save_to_tb(obj)

def table_quchong():
    db_name = "shop_info"
    table_lists = []
    for i in list(db[db_name].find()):
        data = i["data"]
        table_lists.append(data)
    save_to_tb2(table_lists)

def save_to_tb2(data):
    db_name = "shop_info_2"
    db[db_name].insert(data)

def save_to_tb(data):
    db_name = "shop_info_message_2"
    print data
    db[db_name].insert(data)

def unique_table():
    db_name = "shop_info_message"
    db_name2 = "shop_info_message2"
    for i in list(db[db_name].find()):
        for j in list(db[db_name2].find()):
            print i["公司名称"], j["公司名称"]
            # if (i["公司名称"] == j["公司名称"]) and (i["公司地址"] == j["公司地址"]):
            #     return
            # else:
            #     print i
            #     db[db_name2].insert(i)

if __name__ == '__main__':
    standing_tables()
    # unique_table()
    # table_quchong()