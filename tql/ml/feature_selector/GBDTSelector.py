#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : GBDTSelector
# @Time         : 2020/9/23 10:18 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://github.com/microsoft/nni/blob/master/examples/feature_engineering/gbdt_selector/gbdt_selector_test.py

# TODO: cv
# 1. 单特征选择
# 2. 多特征选择
import pandas as pd
from nni.feature_engineering.gbdt_selector import GBDTSelector
from tql.algo_ml.cv import LGBMClassifierCV
from tqdm.auto import tqdm


class LGBSelector(object):
    def __init__(self, params=None, cv=5, cv_seed=777):
        self.params = params
        self.cv = cv
        self.cv_seed = cv_seed

    def fit(self, X, y, feature_names=None, is_univariate=False):  # todo: 目前只支持二分类
        if feature_names is None:
            feature_names = [f'Feat_{i}' for i in X.shape[1]]

        if is_univariate:
            r = []
            for i, feat in tqdm(enumerate(feature_names)):
                X_ = X[:, i:i + 1]

                oof = LGBMClassifierCV(self.params, self.cv, self.cv_seed)
                oof.fit(X_, y)

                r.append((oof.oof_score, feat))

            return pd.DataFrame(sorted(r)[::-1], columns=['score', 'feat_name'])

        else:
            oof = LGBMClassifierCV(self.params, self.cv, self.cv_seed)
            oof.fit(X, y)
            # TODO:
