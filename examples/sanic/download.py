#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : upload
# @Time         : 2019-08-29 11:43
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :


"""
https://www.jianshu.com/p/bc95b1e90129?utm_campaign=maleskine&utm_content=note&utm_medium=seo_notes&utm_source=recommendation
"""

import os
from sanic import Sanic, response
from sanic.response import html, json, redirect, text, raw, file, file_stream

app = Sanic()


@app.route('/<file_name>')
async def handle_request(request, file_name):
    """http://0.0.0.0:9000/baidu.png"""

    print(file_name)
    try:
        return await file_stream(f'./{file_name}')  # file(f'./{file}') # 返回字符串 = open('file_name').read()
    except Exception as e:
        print(e)
        return text(os.popen("ls").read())


@app.route("/raw")
async def get_raw(request):
    """访问此接口后，将会立即下载一个名为raw的文件，里面包含内容 it is raw data"""
    return raw(b"it is raw data")


@app.route("/redirect")
async def get_redirect(request):
    """重定向"""
    return redirect("/raw")


@app.route("/streaming")
async def index(request):
    async def streaming_fn(response):
        response.write('foo')
        response.write('bar')

    return response.stream(streaming_fn, content_type='text/plain')


app.run(host="0.0.0.0", port=9000, debug=True, auto_reload=True)
