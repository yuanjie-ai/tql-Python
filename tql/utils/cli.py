#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : iWork.
# @File         : cli
# @Time         : 2019-06-14 12:20
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import fire

# fire.Fire(lambda obj: type(obj).__name__)


class Calculator(object):

    def __init__(self, arg=0):
        self._arg = arg

    def add(self, x, y):
        return x + y

    def multiply(self, x, y):
        return x * y + self._arg


if __name__ == '__main__':
    # calculator = Calculator()
    fire.Fire(Calculator)
