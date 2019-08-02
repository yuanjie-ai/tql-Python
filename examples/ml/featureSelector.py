#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : featureSelector
# @Time         : 2019-07-26 13:39
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_selection import GenericUnivariateSelect, \
    SelectPercentile, SelectKBest, f_classif, mutual_info_classif, RFE

from lightgbm import LGBMClassifier
import matplotlib.pyplot as plt

sfs = SFS(LGBMClassifier(),
          k_features=10,
          forward=True,
          floating=False,
          verbose=2,
          scoring='roc_auc',
          cv=5,
          n_jobs=-1)

sfs.fit(X, y)
