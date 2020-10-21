#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : featuretools
# @Time         : 2019-07-25 17:05
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

"""

https://www.cnblogs.com/jfdwd/p/11150879.html
https://cloud.tencent.com/developer/article/1471179

https://blog.csdn.net/lanchunhui/article/details/79810550
"""
import pandas as pd
import featuretools as ft

df = pd.DataFrame({'ID': list(range(10))})
print(df.head())
es = ft.EntitySet(id='clients')

# 表必须要有索引, 默认第一列（无索引造索引）
es.entity_from_dataframe('df_test',
                         df,
                         index='ID', make_index=False,  # 指定生成新的索引列
                         variable_types=None,

                         time_index=None,
                         secondary_time_index=None,
                         already_sorted=False)
es.normalize_entity  # 拆表
print(es['df_test'].df)

# Primitive：agg_primitives: 20 个, trans_primitives: 55 个, where_primitives
# 重写：https://docs.featuretools.com/automated_feature_engineering/primitives.html#defining-custom-primitives
from featuretools.primitives import make_agg_primitive, make_trans_primitive

primitives = ft.list_primitives()
pd.options.display.max_colwidth = 100
primitives[primitives['type'] == 'aggregation'].head(10)

from featuretools.selection import remove_low_information_features

# 自定义

