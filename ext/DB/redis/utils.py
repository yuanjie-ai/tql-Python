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

def redis_client(host, port):
    pool = ConnectionPool(host=host, port=port, decode_responses=True)
    r = StrictRedis(connection_pool=pool)
    print("randomkey: ", r.randomkey())
    return r


if __name__ == '__main__':
    r = redis_client('10.118.31.33', 25773)
    for _, v in enumerate(r.keys('br:bd:ark:*')):
        print(v)
        if _ > 5:
            break
