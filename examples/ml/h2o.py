#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : h2o
# @Time         : 2019-09-16 21:12
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split

X, y = make_classification(100000)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.33, random_state=42)

import h2o
from h2o.automl import H2OAutoML
from h2o.estimators import H2OXGBoostEstimator

h2o.init()

aml = H2OAutoML(nfolds=5,
                balance_classes=False,
                class_sampling_factors=None,
                max_after_balance_size=5.0,
                max_runtime_secs=3600,
                stopping_metric="auc",
                stopping_rounds=3,
                seed=666,
                include_algos=None,
                keep_cross_validation_predictions=True,
                verbosity=None)
# h2o.H2OFrame()
"""http://de-33103-tql2dev-0726125601.c5-cloudml.xiaomi.srv/notebooks/ceph/yuanjie/3_H2O/H2O.ipynb"""
aml.train(x=X, y=y,
          training_frame=train,
          leaderboard_frame=test)
