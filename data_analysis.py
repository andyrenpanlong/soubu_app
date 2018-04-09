# -*- coding: utf-8 -*-
from pymongo import MongoClient
import sys
reload(sys)
sys.setdefaultencoding('utf8')

client = MongoClient('127.0.0.1', 27017)
db_soubu = client.soubu
db_soubu_app = client.soubu_app

def save_data(dbname):
    for i in list(db_soubu[dbname].find()):
        print i
        check_update_company_name(i)

def check_update_company_name(company_message):
    db_name = "product_list"
    if len(list(db_soubu_app[db_name].find({"proNum": company_message["proNum"]}))) < 1:
        print u"没找到"
        db_soubu_app[db_name].insert(company_message)
    else:
        print u"找到了"

def shop_info_mess_unique():
    for i in list(db_soubu["shop_info_mess"].find()):
        name = i[u"名称"]
        db_name = "shop_info_message"
        company_message = {}
        company_message["name"] = i[u"名称"]
        company_message["company_name"] = i[u"公司名称"]
        company_message["main_products"] = i[u"主营产品"]
        company_message["main_industry"] = i[u"主营行业"]
        company_message["evaluate"] = i[u"全部评价"]
        company_message["transaction"] = i[u"累计交易"]
        company_message["address"] = i[u"公司地址"]
        company_message["contacts"] = i[u"联系人"]
        company_message["telephone"] = i[u"联系电话"]
        company_message["introduction"] = i[u"公司简介"]
        if len(list(db_soubu_app[db_name].find({"name": name}))) < 1:
            print u"没找到\n"
            db_soubu_app[db_name].insert(company_message)
        else:
            print u"找到了重复数据"

if __name__ == '__main__':
    save_data("product_list222")
    # shop_info_mess_unique()