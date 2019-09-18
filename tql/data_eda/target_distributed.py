#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : target
# @Time         : 2019-09-14 18:36
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


def target_distributed(df, by, target_name='label'):
    _ = df.groupby(by)[target_name].value_counts(1)
    return _
