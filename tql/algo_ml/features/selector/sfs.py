#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : sfs
# @Time         : 2019-07-26 13:41
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
"""
efs的优化版：根据 scoring 筛选特征
顺序特征选择算法的贪婪搜索算法家族，用于减少初始d维特征空间到ķ维特征空间，其中ķ<d 。
特征选择算法背后的动机是自动选择与问题最相关的特征子集。
特征选择的目标是双重的：我们希望通过去除不相关的特征或噪声来提高计算效率并减少模型的泛化误差。
如果嵌入式特征选择（例如，像LASSO这样的正则化惩罚）不适用，则诸如顺序特征选择之类的包装器方法尤其有用。
"""


from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_selection import GenericUnivariateSelect, \
    SelectPercentile, SelectKBest, f_classif, mutual_info_classif, RFE

from lightgbm import LGBMClassifier
import matplotlib.pyplot as plt

X = ...
y = ...

sfs = SFS(LGBMClassifier(),
          k_features=10,
          forward=True,
          floating=False,
          verbose=2,
          scoring='roc_auc',
          cv=3,
          n_jobs=-1)

sfs.fit(X, y)

#  plot
fig1 = plot_sfs(sfs.get_metric_dict(), kind='std_dev')

plt.ylim([0.8, 1])
plt.title('Sequential Forward Selection (w. StdDev)')
plt.show()
