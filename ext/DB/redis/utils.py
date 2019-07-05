#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : utils
# @Time         : 2019-07-02 18:49
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from redis import StrictRedis, ConnectionPool

# 多个Redis实例共享一个连接池，避免每次建立、释放连接的开销。
pool = ConnectionPool(host='10.38.164.94', port=7001, decode_responses=True)
redis = StrictRedis(connection_pool=pool)

print(redis.randomkey())
for _, v in enumerate(redis.keys('br:bd:ark:*')):
    print(v)
    if _ > 5:
        break
