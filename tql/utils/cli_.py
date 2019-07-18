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


def add(x, y, **kwargs):
    """add"""
    print(kwargs)
    return x + y


def multiply(x, y):
    """add"""
    return x * y


def cli():
    fire.Fire()


if __name__ == '__main__':
    fire.Fire()