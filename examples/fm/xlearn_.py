#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : xlearn_
# @Time         : 2019-10-15 16:48
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import numpy as np
import xlearn as xl
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split

# Load dataset
iris_data = load_iris()
X = iris_data['data']
y = (iris_data['target'] == 2)

X_train, \
X_val, \
y_train, \
y_val = train_test_split(X, y, test_size=0.3, random_state=0)

# param:
#  0. binary classification
#  1. model scale: 0.1
#  2. epoch number: 10 (auto early-stop)
#  3. learning rate: 0.1
#  4. regular lambda: 1.0
#  5. use sgd optimization method
fm_model = xl.FMModel(model_type='fm', task='binary', metric='auc', block_size=500,
                      lr=0.2, k=4, reg_lambda=0.1, init=0.1, fold=5, epoch=5, stop_window=2,
                      opt='sgd', nthread=None, n_jobs=4, alpha=1, beta=1, lambda_1=1, lambda_2=1)

# Start to train
fm_model.fit(X_train, y_train,
             eval_set=[X_val, y_val],
             is_lock_free=False)

# Generate predictions
y_pred = fm_model.predict(X_val)
print(y_pred)
