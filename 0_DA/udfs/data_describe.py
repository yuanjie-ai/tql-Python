# coding: utf-8
__title__ = 'data_eda'
__author__ = 'JieYuan'
__mtime__ = '2018/2/13'

from pandas_summary import DataFrameSummary

# 描述性统计
summary = lambda x: DataFrameSummary(x).summary().transpose()
