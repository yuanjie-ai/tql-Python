# coding: utf-8
__title__ = 'list'
__author__ = 'JieYuan'
__mtime__ = '2018/2/13'

from collections import OrderedDict

order_set = lambda x: list(OrderedDict.fromkeys(x)) # 列表有序去重
