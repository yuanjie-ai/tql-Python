#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : _info
# @Time         : 2019-06-20 11:24
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
import os
import socket
from .. import cprint
import platform


class MyInfo(object):

    def __init__(self):
        self.hostname = socket.getfqdn(socket.gethostname())
        self.localhost = socket.gethostbyname(self.hostname)

        print(self.hostname, self.localhost)
        cprint(os.sys.version)
        cprint(platform.platform())


if __name__ == '__main__':
    MyInfo()
