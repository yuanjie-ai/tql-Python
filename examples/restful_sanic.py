#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : restful_sanic
# @Time         : 2019-07-18 10:13
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import jieba
from restful_api import Api


pred1 = lambda **kwargs: kwargs['x'] + kwargs['y']
pred2 = lambda x=1, y=1: x + y
pred3 = lambda text='小米是家不错的公司': jieba.lcut(text)

# 多服务堆叠
api = Api('/post1', pred1)
api = Api('/post2', pred2, app=api.app)
api = Api('/post3', pred3, app=api.app)
api.app.run('0.0.0.0')


# import requests
# json = {'x': 1, 'y': 10}
# requests.post('http://127.0.0.1:8000/post1', json=json).json()
# requests.post('http://127.0.0.1:8000/post2', json=json).json()
# requests.post('http://127.0.0.1:8000/post3', json=json).json()