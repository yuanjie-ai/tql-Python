#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-08-15 10:20
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from iapp import App
import time


app = App()

f1 = lambda **kwargs: 666

def f2(**kwargs):
    with open('./log.txt') as f:
        f.read()
    return
app.add_route("/f1", f1, time=time.ctime())
app.add_route("/f2", f2, time=time.ctime())


app.run()