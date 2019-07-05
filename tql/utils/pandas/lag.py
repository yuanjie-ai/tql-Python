#!/usr/bin/env python
#-*- coding: utf-8 -*-
"""
__title__ = 'lag'
__author__ = 'JieYuan'
__mtime__ = '19-2-14'
"""

def lag(df, by_name, col_name, n=1):
    df = df.copy()
    df[col_name + '_' + str(n)] = df.groupby(by_name)[col_name].shift(n)
    return df