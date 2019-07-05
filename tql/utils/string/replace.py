#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
__title__ = 'replace'
__author__ = 'JieYuan'
__mtime__ = '2019-05-06'
"""
def replace(s, dic):
    return s.translate(str.maketrans(dic))



if __name__ == '__main__':
    print(replace('abcd', {'a': '8', 'd': '88'}))


