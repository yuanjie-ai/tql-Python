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



##############update
a = 666

def update(**kwargs):
    time.sleep(10)

    global a
    a = kwargs
    return a
##############

app = App(1, workers=2)
# update
app.add_route("/update", update, time=time.ctime())

f1 = lambda **kwargs: a
app.add_route("/f1", f1, time=time.ctime())

f2 = lambda **kwargs: 666
app.add_route("/f2", f2, time=time.ctime())
app.run()