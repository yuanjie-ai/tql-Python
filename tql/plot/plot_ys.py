#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'plot_ys'
__author__ = 'JieYuan'
__mtime__ = '2019-04-25'
"""
import numpy as np
import pandas as pd


def plot_ys(y_true, *ys):
    ys = (y_true,) + ys
    columns = ['y%s' % i for i in range(len(ys))]
    df = (pd.DataFrame(np.column_stack(ys), columns=columns)
          .sort_values('y0')
          .reset_index(drop=True))
    df.plot(figsize=(20, 10), subplots=False)
