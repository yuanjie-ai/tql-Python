#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : efs
# @Time         : 2019-07-26 13:49
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

"""
枚举：2^n
"""

from sklearn.neighbors import KNeighborsClassifier
from sklearn.datasets import load_iris
from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS

iris = load_iris()
X = iris.data
y = iris.target

knn = KNeighborsClassifier(n_neighbors=3)

efs1 = EFS(knn,
           min_features=1,
           max_features=4,
           scoring='accuracy',
           print_progress=True,
           cv=5)

efs1 = efs1.fit(X, y)

print('Best accuracy score: %.2f' % efs1.best_score_)
print('Best subset (indices):', efs1.best_idx_)
print('Best subset (corresponding names):', efs1.best_feature_names_)
