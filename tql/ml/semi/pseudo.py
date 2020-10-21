#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : pseudo
# @Time         : 2020/9/6 1:56 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import numpy as np
import pandas as pd
from lightgbm import LGBMClassifier
from sklearn.metrics import roc_auc_score


# 目前只支持二分类 TODO: 回归


class Pseudo(object):

    def __init__(self, X, y, X_test, confidences=(0.99, 0.01), **kwargs):
        self.X = X
        self.y = y
        self.X_test = X_test
        self.confidences = confidences  # 顺序(正，负)，加入训练的样本比例： 正、负比例 # todo: 百分位数或者个数，分正负

    def run(self, n_iter=1):
        X, y = self.X.copy(), self.y.copy()

        stat = []
        for i in range(0, n_iter + 1):
            clf, score, self.test_preds = self.fit_predict(X, y, self.X_test)

            if i == 0:
                print(f"Init Score: {score}")
            else:
                print(f"PseudoLabeling{i} Score: {score}")
                X, y = self.pseudo_labeling(self.test_preds)
                stat.append((i, clf, score))

        self.stat_info = pd.DataFrame(stat, columns=['n_iter', 'model', 'score'])
        print(self.stat_info)

    def fit_predict(self, X, y, X_test, **kwargs):
        """重写继承即可
        :return: clf, score, test_preds
        """
        clf = LGBMClassifier()
        clf.fit(X, y)
        score = roc_auc_score(y, clf.predict_proba(X)[:, 1])  # 验证方式？？？线下训练集CV
        test_preds = clf.predict_proba(X_test)
        return clf, score, test_preds

    def pseudo_labeling(self, preds):
        thresholds = np.quantile(preds, self.confidences)  # 计算上下分位数
        print(f"Thresholds: {thresholds}")

        pos_index = np.where(preds > thresholds[0])[0]
        neg_index = np.where(preds < thresholds[1])[0]

        self.X_pseudo = self.X_test[np.r_[pos_index, neg_index], :]
        self.y_pseudo = np.r_[np.ones(len(pos_index)), np.zeros(len(neg_index))]

        # 合并数据
        print(f"Add: PositiveSamples={len(pos_index)} NegativeSamples={len(neg_index)}\n")

        X = np.r_[self.X, self.X_pseudo]
        y = np.r_[self.y, self.y_pseudo]

        return X, y
