#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : knn
# @Time         : 2019-07-26 14:24
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

"""
https://www.jianshu.com/p/778d39132d66
"""
import numpy as np

from sklearn.neighbors import NearestNeighbors, KNeighborsClassifier, RadiusNeighborsClassifier

# 归一化
X_train = ...
X_test = ...

neigh = NearestNeighbors(5, n_jobs=-1)
neigh.fit(X_train)

dists, _ = neigh.kneighbors(X_train, n_neighbors=5)
mean_dist = dists.mean(axis=1)
max_dist = dists.max(axis=1)
min_dist = dists.min(axis=1)

X_train['300'] = X_train.std(1)
X_train = np.hstack((X_train, mean_dist.reshape(-1, 1), max_dist.reshape(-1, 1), min_dist.reshape(-1, 1)))

test_dists, _ = neigh.kneighbors(X_test, n_neighbors=5)

test_mean_dist = test_dists.mean(axis=1)
test_max_dist = test_dists.max(axis=1)
test_min_dist = test_dists.min(axis=1)

X_test['300'] = X_test.std(1)
X_test = np.hstack((X_test, test_mean_dist.reshape(-1, 1), test_max_dist.reshape(-1, 1), test_min_dist.reshape(-1, 1)))
