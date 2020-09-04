#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : path
# @Time         : 2020/8/18 7:36 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

p = Path('/hdfs/user/h_data_platform/platform/browser/algo/data/biz/xiangkan/Label/社会_train/date=20200816')
with ProcessPoolExecutor(20) as pool:
    df = pd.concat(pool.map(pd.read_parquet, p.glob("part*")))


def get_paths(path, pattern):
    return Path(path).glob(pattern)