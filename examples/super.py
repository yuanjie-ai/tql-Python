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

        print("A:", self.a + self.b)

    @property
    def f(self):
        yield 111111


class B(A):

    def __init__(self, a=100000, **kwargs):
        self.a = a+11111
        print("B:", self.a)
        super().__init__(**kwargs)

        print(self.a)

        pass


if __name__ == '__main__':
    o = B(a=1,b=111)
    print(list(o.f))


