#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'iter'
__author__ = 'JieYuan'
__mtime__ = '18-12-14'
"""
from .utils.xx import xx
from .utils import cprint
from .utils.time import timer
from .utils.pandas_utils import reduce_mem_usage

#########################################################################
import os
import gc
import re
import sys
import json
import pickle
import inspect
import socket
import warnings
import joblib
import numpy as np
import pandas as pd
import jieba
import jieba.analyse as ja

from pathlib import Path
from tqdm.auto import tqdm
from functools import reduce
from functools import lru_cache
from collections import Counter, OrderedDict
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
from sklearn.metrics.pairwise import cosine_similarity

warnings.filterwarnings("ignore")
tqdm.pandas()
#########################################################################

TOP_DIR = os.path.realpath(os.path.dirname("."))

# p = Path(__file__)
get_module_path = lambda path, file=__file__: \
    os.path.normpath(os.path.join(os.getcwd(), os.path.dirname(file), path))
try:
    hostname = socket.getfqdn(socket.gethostname())
    localhost = socket.gethostbyname(hostname)
    ip = localhost
    local_info = {'hostname': hostname, 'localhost': localhost, 'ip': localhost}

    is_dev = True if hostname.__contains__("yuanjie") else False

except Exception as e:
    print(e)

getsize = lambda obj: sys.getsizeof(obj) / 1024 ** 2  # M

getsize_df = lambda df: df.memory_usage().sum() / 1024 ** 2

try:
    import tensorflow as tf

    gpu_list = tf.config.list_physical_devices('GPU')
    if gpu_list:
        use_gpu = int(os.environ.get('USE_GPU', '0'))
    else:
        use_gpu = 0

except Exception as e:
    use_gpu = 0

###################################################################

import seaborn as sns

sns.set(style="darkgrid")  # darkgrid, whitegrid, dark, white,和ticks
sns.set_context('paper')


# sns.plotting_context()
# sns.axes_style()
# plt.style.use('ggplot')

#########################################################################

# 序列化
def df2hdf(df, file='./data.h5'):
    df.to_hdf(file, 'w', complib='blosc', complevel=8)


def reader(fname='./tmp.txt', sep=',', mode='r'):
    with open(fname, mode) as f:
        for l in f:
            yield l.strip().split(sep)


def xpickle_load(file):
    with open(file, 'rb') as f:
        return pickle.load(f)


@xx
def xwrite(iterable, fname, mode='w', glue='\n'):
    with open(fname, mode) as f:
        for item in iterable:
            f.write(str(item) + glue)


@xx
def xpickle_dump(objs, file='tmp.pkl'):
    with open(file, 'wb') as f:
        pickle.dump(objs, f)


# 统计函数: 待补充groupby.agg
# xsummary = xx(lambda iterable: DataFrameSummary(list(iterable) | xDataframe)['iterable'])
xvalue_counts = xx(
    lambda iterable, normalize=False, bins=None: pd.value_counts(list(iterable), normalize=normalize, bins=bins))

__funcs = [sum, min, max, abs, len, np.mean, np.median]
xsum, xmin, xmax, xabs, xlen, xmean, xmedian = [xx(i) for i in __funcs]

xnorm = xx(lambda iterable, ord=2: np.linalg.norm(iterable, ord))
xl1 = xx(lambda iterable: np.linalg.norm(iterable, 1))
xl2 = xx(lambda iterable: np.linalg.norm(iterable, 2))
xcosine = xx(lambda pair_vector: cosine_similarity(pair_vector)[0][1])

xcount = xx(lambda iterable: Counter(list(iterable)))

xunique = xx(lambda iterable: list(OrderedDict.fromkeys(list(iterable))))  # 移除列表中的重复元素(保持有序)
xsort = xx(lambda iterable, reverse=False, key=None: sorted(list(iterable), key=key, reverse=reverse))

xmax_index = xx(lambda x: max(range(len(x)), key=x.__getitem__))  # 列表中最小和最大值的索引
xmin_index = xx(lambda x: min(range(len(x)), key=x.__getitem__))  # 列表中最小和最大值的索引
xmost_freq = xx(lambda x: max(set(x), key=x.count))  # 查找列表中频率最高的值, key作用于set(x), 可类推出其他用法


# gc
@xx
def xgc(iterable):
    del iterable
    gc.collect()


# print
@xx
def xprint(obj, mode=None, bg='blue'):
    if mode:
        for i in obj:
            cprint(i)
            print('\n')
    else:
        cprint(obj, bg)


xtqdm = xx(lambda iterable, desc=None: tqdm(iterable, desc))

# base types
xtuple, xlist, xset = xx(tuple), xx(list), xx(set)

# string
xjoin = xx(lambda s, sep=' ': sep.join(s))
xcut = xx(lambda s, cut_all=False: jieba.lcut(s, cut_all=cut_all))
xtfidf = xx(lambda s, topK=20: ja.tfidf(s, topK=topK))

xsame_key_dict_merge = xx(lambda dics: pd.DataFrame(dics))


@xx
def hump_str(string="a_b", pattern='_'):
    """驼峰式转换"""
    reg = re.compile(pattern)
    _ = reg.sub('', string.title())
    return _.replace(_[0], _[0].lower())


# list transform
xgroup_by_step = xx(lambda ls, step=3: [ls[idx: idx + step] for idx in range(0, len(ls), step)])


# dict
@xx
def xjson(dict_):
    _ = json.dumps(dict_, default=lambda obj: obj.__dict__, sort_keys=True, indent=4)
    return _


@xx
def xSeries(iterable, name='iterable'):
    if isinstance(iterable, pd.Series):
        return iterable
    else:
        return pd.Series(iterable, name=name)


@xx
def xDataframe(iterable, name='iterable'):
    if isinstance(iterable, pd.DataFrame):
        return iterable
    else:
        return pd.DataFrame({name: iterable})


# 高阶函数
xmap = xx(lambda iterable, func: map(func, iterable))
xreduce = xx(lambda iterable, func: reduce(func, iterable))
xfilter = xx(lambda iterable, func: filter(func, iterable))


# multiple
@xx
def xThreadPoolExecutor(iterable, func, max_workers=5):
    """
    with ThreadPoolExecutor(max_workers) as pool:
        pool.map(func, iterable)
    """
    with ThreadPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


@xx
def xProcessPoolExecutor(iterable, func, max_workers=5):
    """
    with ProcessPoolExecutor(max_workers) as pool:
        pool.map(func, iterable)
    """
    with ProcessPoolExecutor(max_workers) as pool:
        return pool.map(func, iterable)


# args
get_args = lambda func: inspect.getfullargspec(func).args
