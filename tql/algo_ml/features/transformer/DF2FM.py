#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : DF2FM
# @Time         : 2019-08-26 20:16
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.datasets import dump_svmlight_file, load_svmlight_file

train, y = make_classification(n_samples=10, n_features=5, n_informative=2, n_redundant=2, n_classes=2, random_state=42)

train = pd.DataFrame(train, columns=['int1', 'int2', 'int3', 's1', 's2'])
train['int1'] = train['int1'].map(int)
train['int2'] = train['int2'].map(int)
train['int3'] = train['int3'].map(int)
train['s1'] = round(np.log(abs(train['s1'] + 1))).map(str)
train['s2'] = round(np.log(abs(train['s2'] + 1))).map(str)
train['clicked'] = y

dump_svmlight_file(pd.get_dummies(train), y, 'svm_output.libsvm', zero_based=False)  # 从1开始编码
dump_svmlight_file(pd.get_dummies(train[['s1', 's2']]), y, 'svm_output.libsvm', zero_based=False)  # 从1开始编码
