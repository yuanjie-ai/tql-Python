#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : BaseOOF
# @Time         : 2019-06-23 20:07
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import StratifiedKFold, RepeatedStratifiedKFold, KFold, cross_val_predict, cross_validate
from sklearn.metrics import roc_auc_score

from xgboost import XGBClassifier


class XGBClassifierCV(object):
    """cross_val_predict"""

    def __init__(self, params=None, cv=5, random_state=None, n_repeats=None):
        self.clf = XGBClassifier()
        self.cv = cv
        if params:
            self.clf.set_params(**params)
        if n_repeats:
            self._kf = RepeatedStratifiedKFold(cv, True, random_state)
            self._num_preds = cv * n_repeats
        else:
            self._kf = StratifiedKFold(cv, True, random_state)
            self._num_preds = cv

    def fit(self, X, y, X_test=None, feval=roc_auc_score, sample_weight=None, eval_metric='auc',
            early_stopping_rounds=300, verbose=100, xgb_model=None, sample_weight_eval_set=None, callbacks=None):
        """输入数组"""
        self.best_info = {}
        if X_test is None:
            X_test = X[:1]

        self.oof_train = np.zeros(len(X))
        self.oof_test = np.zeros((len(X_test), self._num_preds))
        for n_fold, (train_index, valid_index) in enumerate(self._kf.split(X, y)):
            if verbose:
                print("\033[94mFold %s started at %s\033[0m" % (n_fold + 1, time.ctime()))
            X_train, y_train = X[train_index], y[train_index]
            X_valid, y_valid = X[valid_index], y[valid_index]
            eval_set = [(X_train, y_train), (X_valid, y_valid)]

            ########################################################################
            self.clf.fit(X_train, y_train, sample_weight, eval_set=eval_set, eval_metric=eval_metric,
                         early_stopping_rounds=early_stopping_rounds, verbose=verbose,
                         xgb_model=xgb_model, sample_weight_eval_set=sample_weight_eval_set,
                         callbacks=callbacks)

            self.oof_train[valid_index] = self.clf.predict_proba(X_valid)[:, 1]
            self.oof_test[:, n_fold] = self.clf.predict_proba(X_test)[:, 1]

            # best info
            # print(self.clf.evals_result_)
            self.best_info.setdefault('best_iteration', []).append(self.clf.best_iteration)
            self.best_info.setdefault('best_score_valid', []).append(self.clf.best_score)
            ########################################################################

        # 输出 测试集 oof
        self.oof_test_rank = (pd.DataFrame(self.oof_test).rank().mean(1) / len(self.oof_test)).values
        self.oof_test = self.oof_test.mean(1)

        assert len(X) == len(self.oof_train)
        assert len(X_test) == len(self.oof_test)

        # 计算 训练集 oof 得分
        if feval:
            self.oof_score = feval(y, self.oof_train)
            print("\n\033[94mScore Info:\033[0m")
            print(f"\033[94m     {self.cv:>2} CV: {self.oof_score:.6f}\033[0m")

            _ = np.array(self.best_info['best_iteration'])
            print(f"\033[94m      Iter: {_.mean():.0f} +/- {_.std():.0f}\033[0m")

            _ = np.array(self.best_info['best_score_valid'])
            print(f"\033[94m     Valid: {_.mean():.6f} +/- {_.std():.6f} \033[0m\n")

        return self.oof_score

    def oof_submit(self, ids, pred_ranking=False, file=None, preds=None):
        """preds藏分用"""
        if file is None:
            file = f'submit_cv{self.cv}_{self.oof_score}.csv'
        print(f'Save {file} ...')

        if preds is None:
            preds = self.oof_test_rank if pred_ranking else self.oof_test

        if not isinstance(ids, pd.DataFrame):
            ids = pd.DataFrame(ids)
        ids.assign(preds=preds).to_csv(file, index=False, header=False)

    @property
    def oof_train_and_test(self):
        return np.r_[self.oof_train, self.oof_test]

    def oof_save(self, file='./oof_train_and_test.csv'):
        pd.DataFrame(self.oof_train_and_test, columns=['oof_train_and_test']).to_csv(file, index=False)

    def plot_feature_importances(self, feature_names=None, topk=20, figsize=(10, 6), pic_name=None):
        columns = ['Importances', 'Features']
        importances = self.clf.feature_importances_.tolist()
        if feature_names is None:
            feature_names = list(map(lambda x: f'F_{x}', range(len(importances))))
        _ = list(zip(importances, feature_names))
        df = pd.DataFrame(_, columns=columns).sort_values('Importances', 0, False)

        plt.figure(figsize=figsize)
        sns.barplot(*columns, data=df[:topk])
        plt.title('Features Importances\n')
        plt.tight_layout()
        if pic_name is None:
            plt.savefig(f'importances_{self.oof_score}.png')


if __name__ == "__main__":
    from sklearn.datasets import make_classification

    X, y = make_classification()
    X_test, _ = make_classification()

    clf = XGBClassifierCV({'n_estimators': 1000})
    clf.fit(X, y, X_test)
