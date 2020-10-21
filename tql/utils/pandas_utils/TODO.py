#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'TODO'
__author__ = 'JieYuan'
__mtime__ = '2019-04-23'
"""
import pandas as pd

df = pd.DataFrame()
# 分析两个类别型特征得到新特征rate
df.groupby('author')['category'] \
    .agg({'rate': lambda x: pd.value_counts(x, normalize=True)[:1]}) \
    .reset_index()
