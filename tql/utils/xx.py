#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'x'
__author__ = 'JieYuan'
__mtime__ = '18-12-14'
"""

import functools

class xx:
    """I am very like a linux pipe"""

    def __init__(self, function):
        self.function = function
        functools.update_wrapper(self, function)

    def __ror__(self, other):
        return self.function(other)

    def __call__(self, *args, **kwargs):
        return xx(lambda x: self.function(x, *args, **kwargs))


if __name__ == '__main__':
    @xx
    def xfunc1(x):
        _ = x.split()
        print(_)
        return _


    @xx
    def xfunc2(x):
        _ = '>>'.join(x)
        print(_)
        return _


    'I am very like a linux pipe' | xfunc1 | xfunc2
