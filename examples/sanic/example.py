#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : example
# @Time         : 2019-09-12 11:37
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import os
from sanic import Sanic, response
from sanic.response import html, json, redirect, text, raw, file, file_stream

app = Sanic()


@app.route('/get')
async def get_test(request):
    title = request.args.get('title')
    return response.json([{'model_name': title}])



app.run()
