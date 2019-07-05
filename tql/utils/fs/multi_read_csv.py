#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'multi_read_csv'
__author__ = 'JieYuan'
__mtime__ = '19-3-15'
"""

import pandas as pd
from concurrent.futures import ProcessPoolExecutor

from tqdm import tqdm
from functools import partial


def multi_read_csv(files, workers=2, **kwargs):
    read_func = partial(pd.read_csv, **kwargs)
    return list(map(read_func, tqdm(files)))
