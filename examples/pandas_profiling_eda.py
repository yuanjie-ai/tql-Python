#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : pandas_profiling
# @Time         : 2019-07-08 10:56
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import numpy as np
import pandas as pd
import pandas_profiling

df = pd.DataFrame(
    np.random.rand(100, 5),
    columns=['a', 'b', 'c', 'd', 'e']
)



profile = df.profile_report(title='EAD')
profile.to_file(output_file="output.html")