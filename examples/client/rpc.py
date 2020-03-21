#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : rpc
# @Time         : 2020-02-04 15:47
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 客户端、服务端 https://github.com/Cloudox/PythonRPCStudy


import os
from xmlrpc.server import SimpleXMLRPCServer
from socketserver import ThreadingMixIn, ForkingMixIn


class ThreadXMLRPCServer(ThreadingMixIn, SimpleXMLRPCServer):
    """多线程"""
    pass


# shell
def sh(cmd):
    with os.popen(cmd) as f:
        return f.read().split()

if __name__ == '__main__':
    server = ThreadXMLRPCServer(('0.0.0.0', 7777), allow_none=True)
    # 注册函数
    server.register_function(sh, 'sh')
    print("服务端")
    # 保持等待调用状态
    server.serve_forever()

    # from xmlrpc.client import ServerProxy
    #
    # client = ServerProxy('http://10.114.38.22:7777')
    # client.sh('ls')