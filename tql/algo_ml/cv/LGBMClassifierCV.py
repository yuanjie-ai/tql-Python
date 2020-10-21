#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : OOFlgb
# @Time         : 2019-06-23 23:41
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

from lightgbm import LGBMClassifier
from tqdm.auto import tqdm

import os
import socket

if socket.gethostname() == 'yuanjie-Mac.local':
    os.environ['KMP_DUPLICATE_LIB_OK'] = 'TRUE'


class LGBMClassifierCV(object):
    """cross_val_predict"""

    def __init__(self, params=None, cv=5, cv_seed=None, n_repeats=None):
        self.clf = LGBMClassifier()
        self.cv = cv
        if params:
            self.clf.set_params(**params)
        if n_repeats:
            self._kf = RepeatedStratifiedKFold(cv, shuffle=True, random_state=cv_seed)
            self._num_preds = cv * n_repeats
        else:
            self._kf = StratifiedKFold(cv, shuffle=True, random_state=cv_seed)
            self._num_preds = cv

    def fit(self, X, y, X_test=None, feval=roc_auc_score, fix_valid_index=None, sample_weight=None, init_score=None,
            eval_metric='auc', early_stopping_rounds=300, verbose=100, feature_name='auto', categorical_feature='auto',
            callbacks=None):
        """
        :param X: 数组
        :param y:
        :param X_test:
        :param feval:
        :param fix_valid_index: 默认折外为验证集，可添加验证集范围（指定其在X里的index）
        :return:
        """
        self.best_info = {}
        self.feature_importances = 0
        if X_test is None:
            X_test = X[:1]

        self.oof_train = np.zeros(len(X))
        self.oof_test = np.zeros((len(X_test), self._num_preds))
        for n_fold, (train_index, valid_index) in enumerate(self._kf.split(X, y)):
            if verbose:
                print("\033[94mFold %s started at %s\033[0m" % (n_fold + 1, time.ctime()))

            # 设置valid早停范围：原生X索引
            if fix_valid_index is not None:
                valid_index = list(set(fix_valid_index) & set(valid_index))  # 线下 + 线上验证集

            X_train, y_train = X[train_index], y[train_index]
            X_valid, y_valid = X[valid_index], y[valid_index]
            eval_set = [(X_train, y_train), (X_valid, y_valid)]

            ########################################################################
            self.clf.fit(X_train, y_train, sample_weight, init_score, eval_set, eval_names=('Train', 'Valid'),
                         eval_sample_weight=None, eval_class_weight=None, eval_init_score=None, eval_metric=eval_metric,
                         early_stopping_rounds=early_stopping_rounds, verbose=verbose, feature_name=feature_name,
                         categorical_feature=categorical_feature, callbacks=callbacks)

            self.oof_train[valid_index] = self.clf.predict_proba(X_valid)[:, 1]
            self.oof_test[:, n_fold] = self.clf.predict_proba(X_test)[:, 1]

            # best info
            self.best_info.setdefault('best_iteration', []).append(self.clf.best_iteration_)
            # todo: 支持多分类
            self.best_info.setdefault('best_score_train', []).append(self.clf.best_score_['Train']['auc'])
            self.best_info.setdefault('best_score_valid', []).append(self.clf.best_score_['Valid']['auc'])

            # feature importances
            self.feature_importances += self.clf.feature_importances_ / self.cv

            ########################################################################

        # 输出 测试集 oof
        self.oof_test_rank = (pd.DataFrame(self.oof_test).rank().mean(1) / len(self.oof_test)).values
        self.oof_test = self.oof_test.mean(1)

        assert len(X) == len(self.oof_train)
        assert len(X_test) == len(self.oof_test)

        # 计算 训练集 oof 得分
        if feval is not None and verbose > 0:
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

    def plot_feature_importances(self, feature_names=None, topk=20, figsize=None, pic_name=None):
        columns = ['Importances', 'Features']
        importances = self.feature_importances.tolist()
        if feature_names is None:
            feature_names = list(map(lambda x: f'F_{x}', range(len(importances))))

        _ = sorted(zip(importances, feature_names), reverse=True)
        self.df_feature_importances = pd.DataFrame(_, columns=columns)

        plt.figure(figsize=(14, topk // 5) if figsize is None else figsize)
        sns.barplot(*columns, data=self.df_feature_importances[:topk])
        plt.title('Features Importances\n')
        plt.tight_layout()
        if pic_name is None:
            plt.savefig(f'importances_{self.oof_score}.png')

    @classmethod
    def opt_cv(cls, X, y, X_test=None, cv_list=range(3, 16), params=None, cv_seed=777, topk=5):

        oofs = []
        for cv in tqdm(cv_list, desc='opt cv'):  # range(3, 16):
            oof = cls(params, cv, cv_seed=cv_seed)
            oof.fit(X, y, X_test, verbose=0)
            oofs.append((oof.oof_score, cv, oof))

        return sorted(oofs)[::-1][:topk]


if __name__ == "__main__":
    from sklearn.datasets import make_classification

    X, y = make_classification(1000, random_state=666)
    #
    clf = LGBMClassifierCV()
    # clf.fit(X, y, fix_valid_index=range(500))
    # # print(clf.valid_index)
    # # print(clf.valid_index_)
    # print(clf.feature_importances)
    # print(clf.clf.feature_importances_)
    # clf.plot_feature_importances()

    clf.opt_cv(X, y)
