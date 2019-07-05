#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'daily'
__author__ = 'JieYuan'
__mtime__ = '2019-05-24'
"""

# 1. 每5分钟爬一次
# 2. 每天存文件
import time
import pendulum
import pandas as pd
from iwork.crawler.HotSpider import HotSpider

get_time = lambda t: pendulum.from_timestamp(t, 'Asia/Shanghai')

query = '正能量'
hs = HotSpider(query)

data = pd.DataFrame()
while 1:
    try:
        df = hs.df_sites_info()
        dt = get_time(time.time())

        print("我睡一会😪💤")
        time.sleep(10)

        if dt.add(minutes=5).date() < dt.date():
            continue
        else:
            print("我取")
            data = pd.concat([df, data]).drop_duplicates('title')
            data.to_csv("positive energy: %s" % dt.date(), '\t', index=False)

    except Exception as e:
        print(e)
        raise Exception("爬取异常")