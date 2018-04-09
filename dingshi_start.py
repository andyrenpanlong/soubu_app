# -*- coding: utf-8 -*-
from scrapy import cmdline
import time
import os

def start_process():
    os.system('python dianpu.py')
    time.sleep(60*3600) # 每隔一小时重新执行命令，防止进程中断
    start_process()


start_process()
