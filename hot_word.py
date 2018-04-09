# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from pymongo import MongoClient
import requests
from cookielib import CookieJar
import json
import time
import urllib
import urllib2
import ssl
import sys
from soubu_setting import headers
reload(sys)
sys.setdefaultencoding('utf8')

# 搜布网app数据抓取
requests = requests.Session()
ssl._create_default_https_context = ssl._create_unverified_context

headers = headers

def get_soubu_hot_word(url):
    loadData = "params=%7B%22type%22%3A2%2C%22requestId%22%3A%2215204062005412071796704%22%2C%22serverId%22%3A%22%22%7D"
    response = requests.post(url, data=loadData, headers=headers, verify=False)
    data_obj = json.loads(response.text)
    print data_obj, data_obj["msg"]
    print data_obj["result"]
    print data_obj["sec"]
    print data_obj["status"]
    data = data_obj["result"]["data"]
    soubu_hot_word_save(data)


def soubu_hot_word_save(data):
    client = MongoClient('127.0.0.1', 27017)
    db = client.soubu
    db_name = "hot_word"
    db[db_name].insert(data)


if __name__ == '__main__':
    url = "https://api.isoubu.com/sbapi/Api/Index/get_hot_word"
    get_soubu_hot_word(url)
