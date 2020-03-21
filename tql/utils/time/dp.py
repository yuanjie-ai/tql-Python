#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : Python.
# @File         : dp
# @Time         : 2020-03-13 10:37
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import time
import datetime


class dateprocess:
    # datetime 转 string
    def datetime2str(self, input_datetime):
        input_str = input_datetime.strftime('%Y-%m-%d %H:%M:%S')
        return input_str
        # string 转 datetime

    def str2datetime(self, input_str):
        input_dt = datetime.datetime.strptime(input_str, '%Y-%m-%d %H:%M:%S')
        return input_dt

    # string 转 timestamp
    def str2timestamp(self, input_str):
        timeArray = time.strptime(input_str, "%Y-%m-%d %H:%M:%S")
        timestamp = int(time.mktime(timeArray))
        return timestamp

    # timestamp 转 string
    def timestamp2str(self, input_str):
        input_dt = datetime.datetime.fromtimestamp(input_str)
        return input_dt

    # datetime 转 time_tuple
    def datetime2time_tuple(self, dt):
        input_dt = dt.timetuple()
        return input_dt

    # str 转 time_tuple
    def str2time_tuple(self, data_str):
        input_str = time.strptime(data_str, '%Y-%m-%d %H:%M:%S')
        return input_str
        # timestap 转 time_tuple

    def timestamp2time_tuple(self, data_timestamp):
        input_str = time.localtime(data_timestamp)
        return input_str
        # time_tuple 转 timestamp

    def time_tuple2timestamp(self, time_tuple):
        input_str = int(time.mktime(time_tuple))
        return input_str
        # 比如昨天同一时刻

    def days_difference(self, n):
        now_dt = datetime.datetime.now() - datetime.timedelta(days=n)
        return now_dt

    # 比如一个小时之前
    def hours_difference(self, n):
        now_dt = datetime.datetime.now() - datetime.timedelta(hours=n)
        return now_dt

if __name__ == '__main__':

    data = dateprocess()
    now = datetime.datetime.now()
    data_str = data.datetime2str(now)
    print('-----------data_str--------------')
    print(data_str)