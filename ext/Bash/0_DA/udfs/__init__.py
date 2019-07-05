# -*- coding: utf-8 -*-
# python -m cProfile filename.py

# import base packages

import warnings
# warnings.filterwarnings("ignore")
def ignore_warn(*args, **kwargs):
    pass
warnings.warn = ignore_warn

import os
import re
import time
import numpy as np
import pandas as pd
from pathlib import Path
import matplotlib.pyplot as plt

from sklearn.preprocessing import *
from sklearn.pipeline import make_pipeline, Pipeline
from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score


# 目录树
def lst_tree(p='..', n=0):
    p = Path(p)
    if p.is_file():  # 判断是否是文件
        print('|' + '\t|' * n + '-' * 4 + p.name)
    elif p.is_dir():  # 判断是否是目录
        print('|' + '\t|' * n + '-' * 4 + str(p.relative_to(p.parent)) + '\\')
        for pt in p.iterdir():
            lst_tree(pt, n + 1)  # 递归
