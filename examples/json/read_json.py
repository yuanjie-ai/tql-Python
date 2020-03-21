#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : read_json
# @Time         : 2020-01-08 16:17
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import pandas as pd

# 读取多行json
df = pd.read_json(
    "/Users/yuanjie/Desktop/part-00000-c9133dfd-7a45-4634-8566-cd8e09e38110-c000.json",
    'records',
    lines=True
)


