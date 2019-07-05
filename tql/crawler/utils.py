#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'utils'
__author__ = 'JieYuan'
__mtime__ = '2019-05-15'
"""
# from fake_useragent import UserAgent


class SpiderConfig(object):
    # ua = UserAgent()

    def __init__(self):
        pass

    @property
    def headers(self):
        return {'user-agent': self.ua.random}

    @property
    def proxies(self):
        pass

    @property
    def cookies(self):
        pass


# import random
# import requests
#
# ips = [("118.190.95.35", 9001), ]
#
# try:
#     requests.adapters.DEFAULT_RETRIES = 3
#     host, port = random.choice(ips)
#     proxies = {"http": "http://%s:%s" % (host, port)}
#
#     r = requests.get("http://icanhazip.com/", timeout=8, proxies=proxies)
#     if host == r.text.strip():
#         print('代理有效：%s' % proxies )
#     else:
#         print("代理无效")
# except:
#     print("代理无效")
