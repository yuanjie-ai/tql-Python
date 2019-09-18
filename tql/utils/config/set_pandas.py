#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : pd_set
# @Time         : 2019-06-20 11:27
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import pandas as pd


def set_pandas(max_rows=256, max_columns=64):
    """
    pd.set_option('display.max_rows', 1024)
    pd.set_option('display.max_columns', 128)
    pd.set_option('max_colwidth', 128)  # 列宽
    # pd.set_option('expand_frame_repr', False)  # 允许换行显示
    """
    pd.set_option('display.max_rows', max_rows)
    pd.set_option('display.max_columns', max_columns)
    pd.set_option('max_colwidth', 128)  # 列宽
    # pd.set_option('expand_frame_repr', False)  # 允许换行显示
    print('Setting Success!')
