#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : LGBSelector
# @Time         : 2020/10/13 7:34 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import pandas as pd
from tqdm.auto import tqdm

from tql.algo_ml.cv import LGBMClassifierCV


class FS(object):

    def __init__(self, sorted_feats_by_feature_importances, max_features=100, early_stopping_steps=-1, params=None,
                 cv=5, cv_seed=777):
        self.sorted_feats = sorted_feats_by_feature_importances
        self.max_features = max_features
        self.early_stopping_steps = early_stopping_steps
        self.clf = LGBMClassifierCV(params, cv, cv_seed)
        self.df_oofs = pd.DataFrame()
        self.selected_features_ = []

    def fit(self, train_df, y, test_df=None):
        step = 0
        score = 0
        self.scores = []
        print(f"Selecting until scores don't improve for {self.early_stopping_steps} rounds.")

        tqdm_ = tqdm(list(enumerate(self.sorted_feats)))
        for i, feat in tqdm_:
            tqdm_.set_description(feat)
            self.selected_features_.append(feat)

            self.clf.fit(
                train_df[self.selected_features_].values, y,
                test_df[self.selected_features_].values if test_df is not None else None,
                early_stopping_rounds=64, verbose=0
            )

            if self.clf.oof_score > score:
                step = 0  # 置0
                score = self.clf.oof_score
                self.scores.append(score)  # 历史得分方便画图

                if test_df is not None:
                    self.df_oofs[f"oof_{i}"] = self.clf.oof_train_and_test  # 方便作stacking

            else:
                self.selected_features_.pop(-1)
                step += 1

                if len(self.selected_features_) == self.max_features:
                    break

                if self.early_stopping_steps > 0:
                    if step == self.early_stopping_steps:  # 累计n个特征未提升终止特征选择
                        break
