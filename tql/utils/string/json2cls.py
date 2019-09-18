#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : json2cls
# @Time         : 2019-09-03 12:36
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


class CreateOrder(object):
    def __init__(self):
        self.success = None
        self.item = None


co = CreateOrder()
co.__dict__ = {'success': True,
               'item': {'id': '1f4652c2f841f94f77b29a7836ffb971',
                        'title': '“乱港分子”黄之锋抵台 将拜会民进党',
                        'url': 'https://mb.yidianzixun.com/article/0N7BdC2A?s=mb&appid=mibrowser&miref=newsin_push_model',
                        'category': ['时政'],
                        'publishTime': '2019-09-03 11:03:02',
                        'keywords': ['时政', '香港', '台湾'],
                        'source': '快讯',
                        'valid': True,
                        'userTags': ['时政', '香港', '台湾'],
                        'crawlTime': 1567479784181,
                        'cpApi': 'cn-browser-push',
                        'isReservedDoc': True,
                        'updateTime': 1567479784181,
                        'bizIndexName': 'BROWSER_NEWS'}}

print(co.success)
print(co.item)
