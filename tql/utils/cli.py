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
    """doc"""

    def __init__(self, arg=0, **kwargs):
        """

        :param arg:
        """
        self.arg = arg
        print(kwargs)

    def add(self, x, y, **kwargs):
        """add"""
        print(kwargs)
        return x + y

    def multiply(self, x, y):
        """add"""
        return x * y + self.arg

    def get_list(self, x):
        print(type(x))
        return x


def cli():
    fire.Fire(Calculator)


if __name__ == '__main__':
    # calculator = Calculator()
    fire.Fire(Calculator)

# 方法用 - 分割
"""
python cli.py --arg 0 --a 1 
- add 1 2 --b 1000
"""
