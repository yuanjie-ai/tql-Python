# coding: utf-8
__title__ = 'data_save'
__author__ = 'JieYuan'
__mtime__ = '2018/2/13'


# 数据存储

def as_hdf(df, path):
    df.to_hdf(path, 'w', complib='blosc', complevel=5)
