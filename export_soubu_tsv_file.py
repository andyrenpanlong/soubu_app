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

# 导出店铺信息
def export_shop_info():
    writer = tsv.TsvWriter(open("shop_info.tsv", "w"))
    # 添加评论
    writer.comment("站点名称, 热卖款式：url(链接), product_type(产品类型), address(站点)")
    writer.line("url", "product_type", "address")
    client = MongoClient('127.0.0.1', 27017)
    db = client.seventeen_zwd
    db_name = "station_message"
    for i in list(db[db_name].find()):
        data = []
        data.append(i["url"])
        data.append(i["product_type"])
        data.append(i["address"])
        writer.list_line(data)
    writer.close()

# 导出产品信息
def export_product_info():
    writer = tsv.TsvWriter(open("shop_type_message.tsv", "w"))
    # 添加评论
    writer.comment("市场，热卖档口，档口种类信息：url(链接), type(种类), market(市场), address(站点)")
    writer.line("url", "type", "market", "address")
    client = MongoClient('127.0.0.1', 27017)
    # 连接所需数据库,sf_fy（顺丰-丰眼）为数据库名称，
    db = client.seventeen_zwd
    db_name = "shop_type_message"
    for i in list(db[db_name].find()):
        print json.dumps(i["type"])
        data = []
        data.append(i["url"])
        data.append(json.dumps(i["type"], ensure_ascii=False))
        data.append(json.dumps(i["market"], ensure_ascii=False))
        data.append(i["address"])
        writer.list_line(data)
    writer.close()



if __name__ == '__main__':
    # export_station_red_style()
    # export_shop_type_message()
    export_shop_message()
    # export_daifa_message()
    # export_chuzu_message()
    # clean_shop_message_data()