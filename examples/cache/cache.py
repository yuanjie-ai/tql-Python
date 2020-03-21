#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : cache
# @Time         : 2020-01-10 16:13
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : http://kuanghy.github.io/2016/04/20/python-cache


import random
import datetime


class MyCache:
    """缓存类"""

    def __init__(self):
        # 用字典结构以 kv 的形式缓存数据
        self.cache = {}
        # 限制缓存的大小，因为缓存的空间有限
        # 所以当缓存太大时，需要将旧的缓存舍弃掉
        self.max_cache_size = 10

    def __contains__(self, key):
        """根据该键是否存在于缓存当中返回 True 或者 False"""
        return key in self.cache

    def get(self, key):
        """从缓存中获取数据"""
        data = self.cache[key]
        data["date_accessed"] = datetime.datetime.now()
        return data["value"]

    def add(self, key, value):
        """更新该缓存字典，如果缓存太大则先删除最早条目"""
        if key not in self.cache and len(self.cache) >= self.max_cache_size:
            self.remove_oldest()
        self.cache[key] = {
            'date_accessed': datetime.datetime.now(),
            'value': value
        }

    def remove_oldest(self):
        """删除具备最早访问日期的输入数据"""
        oldest_entry = None

        for key in self.cache:
            if oldest_entry is None:
                oldest_entry = key
                continue
            curr_entry_date = self.cache[key]['date_accessed']
            oldest_entry_date = self.cache[oldest_entry]['date_accessed']
            if curr_entry_date < oldest_entry_date:
                oldest_entry = key

        self.cache.pop(oldest_entry)

    @property
    def size(self):
        """返回缓存容量大小"""
        return len(self.cache)