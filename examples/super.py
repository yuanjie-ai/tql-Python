#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2019-06-23 21:36
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


class A:

    def __init__(self, a=1, b=2):
        self.a = a
        self.b = b

        print(self.a + self.b)

    @property
    def f(self):
        yield 111111


class B(A):

    def __init__(self, a=100000, **kwargs):
        self.a = a+11111
        super().__init__(**kwargs)

        print(self.a)

        pass


if __name__ == '__main__':
    print(B(a=1,b=111))


