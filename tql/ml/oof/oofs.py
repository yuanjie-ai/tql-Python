#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : LGBMClassifierOOF
# @Time         : 2020/9/5 8:40 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from tql.ml.oof.base_oof import BaseOOF
from lightgbm import LGBMClassifier
from xgboost import XGBClassifier
from catboost import CatBoostClassifier


class CatBoostClassifierOOF(BaseOOF):

    def fit_predict(self, X_train, y_train, X_valid, y_valid, X_test, **kwargs):
        clf = CatBoostClassifier(thread_count=30)  # TODO: embedding_features
        if self.params is not None:
            clf.set_params(**self.params)
            # print(clf.get_params())

        # eval_set = [(X_train, y_train), (X_valid, y_valid)]
        self.clf = clf.fit(X_train, y_train,
                           eval_set=(X_valid, y_valid),  # CatBoostError: Multiple eval sets are not supported on GPU
                           # Only one of parameters ['verbose', 'logging_level', 'verbose_eval', 'silent'] should be set
                           verbose=100,
                           early_stopping_rounds=100,
                           use_best_model=True,
                           plot=True,
                           **kwargs
                           )
        # evals_result = self.clf.evals_result()

        valid_predict = clf.predict_proba(X_valid)
        test_predict = clf.predict_proba(X_test)
        return valid_predict, test_predict


class LGBMClassifierOOF(BaseOOF):

    def fit_predict(self, X_train, y_train, X_valid, y_valid, X_test, **kwargs):
        clf = LGBMClassifier()
        if self.params is not None:
            clf.set_params(**self.params)
            # print(clf.get_params())

        eval_set = [(X_train, y_train), (X_valid, y_valid)]
        self.clf = clf.fit(
            X_train, y_train,
            eval_set=eval_set,
            eval_metric=None,
            eval_names=('Train', 'Valid'),
            verbose=100,
            early_stopping_rounds=100,  # fit_params
            **kwargs  # TODO: set_params
        )

        valid_predict = clf.predict_proba(X_valid)
        test_predict = clf.predict_proba(X_test)
        return valid_predict, test_predict

    def plot_feature_importances(self):
        # TODO
        pass


class XGBClassifierOOF(BaseOOF):

    def fit_predict(self, X_train, y_train, X_valid, y_valid, X_test, **kwargs):
        clf = XGBClassifier()
        if self.params is not None:
            clf.set_params(**self.params)
            # print(clf.get_params())

        eval_set = [(X_train, y_train), (X_valid, y_valid)]
        self.clf = clf.fit(
            X_train, y_train,
            eval_set=eval_set,
            eval_metric=None,
            verbose=100,
            early_stopping_rounds=100
        )
        # evals_result = self.clf.evals_result()

        valid_predict = clf.predict_proba(X_valid)
        test_predict = clf.predict_proba(X_test)
        return valid_predict, test_predict


if __name__ == '__main__':
    from sklearn.datasets import load_iris

    X, y = load_iris(return_X_y=True)
    X, y = X[:100], y[:100]

    oofs = [
        # LGBMClassifierOOF(X, y, params={'metrics': ['auc']}),
        # XGBClassifierOOF(X, y, params={'eval_metric': 'auc'})
        CatBoostClassifierOOF(X, y, params={'eval_metric': 'AUC'})
    ]

    for clf_oof in oofs:
        clf_oof.run()
