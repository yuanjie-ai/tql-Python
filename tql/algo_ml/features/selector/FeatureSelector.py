#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : sfs
# @Time         : 2019-07-26 13:41
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import joblib
from sklearn.feature_selection import RFECV
from mlxtend.feature_selection import ExhaustiveFeatureSelector as EFS
from mlxtend.feature_selection import SequentialFeatureSelector as SFS
from mlxtend.plotting import plot_sequential_feature_selection as plot_sfs
from sklearn.neighbors import NearestNeighbors
from sklearn.feature_selection import GenericUnivariateSelect, \
    SelectPercentile, SelectKBest, f_classif, mutual_info_classif, RFE

from lightgbm import LGBMClassifier
import matplotlib.pyplot as plt


class FeatureSelector(object):

    def __init__(self, estimator=LGBMClassifier(n_jobs=30), scoring='roc_auc', selector_name='rfe', cv_worker=1,
                 step=1):
        """

        :param estimator:
        :param scoring:
        :param selector: {'sfs', 'efs', 'rfe'} # rfe 可以粗排一下用gpu加速
        :param cv_worker: gpu要设为1
        """
        self.selector_name = selector_name
        if selector_name == 'sfs':
            """
            efs的优化版：根据 scoring 筛选特征
            顺序特征选择算法的贪婪搜索算法家族，用于减少初始d维特征空间到ķ维特征空间，其中ķ<d 。
            特征选择算法背后的动机是自动选择与问题最相关的特征子集。
            特征选择的目标是双重的：我们希望通过去除不相关的特征或噪声来提高计算效率并减少模型的泛化误差。
            如果嵌入式特征选择（例如，像LASSO这样的正则化惩罚）不适用，则诸如顺序特征选择之类的包装器方法尤其有用。
            """
            self.selector = SFS(estimator,
                                scoring=scoring,
                                cv=5,
                                n_jobs=cv_worker,
                                verbose=2,

                                k_features='best',
                                forward=True,
                                floating=False,
                                )
        elif selector_name == 'efs':  # 枚举：2^n
            self.selector = EFS(estimator,
                                scoring=scoring,
                                cv=5,
                                n_jobs=cv_worker,
                                print_progress=True,

                                max_features=1000
                                )
        elif selector_name == 'rfe':  # 根据树模型特征重要性等权重信息筛选特征
            """https://www.jianshu.com/p/025395835591
            # 打印的是相应位置上属性的排名
            print(rfe.ranking_)
            # 属性选择的一种模糊表示，选择的是true，未选择的是false
            print(rfe.support_)
            # 第1个属相的排名
            print(rfe.ranking_[1])
            # 外部估计函数的相关信息
            print(rfe.estimator_)
            """
            """https://www.kaggle.com/roydatascience/recursive-feature-selection-new-transactions-elo"""
            self.selector = RFECV(
                estimator,
                scoring=scoring,
                cv=5,
                n_jobs=cv_worker,
                verbose=2,

                step=step,  # 每次迭代要删除的特征数/占比
            )

    def fit(self, X, y, saved_selector_name=None):
        self.dim = X.shape[1]
        self.selector.fit(X, y)  # 可重写 fit
        if saved_selector_name:
            joblib.dump(self.selector, saved_selector_name)

    def plot(self):
        if self.selector_name == 'rfe':
            step = self.selector.step if self.selector.step > 1 else int(self.selector.step * self.dim)
            plt.figure(figsize=(12, 9))
            plt.xlabel(f'Number of features tested x {step}')
            plt.ylabel('Cross-validation score')
            plt.plot(range(1, len(self.selector.grid_scores_) + 1), self.selector.grid_scores_)
            # plt.savefig('ELO-lgbmcv-02.png', dpi=150)

        else:
            plot_sfs(self.selector.get_metric_dict(), kind='std_dev')
            plt.ylim([0.8, 1])
            plt.title('Sequential Forward Selection (w. StdDev)')

        plt.show()


if __name__ == '__main__':
    from sklearn.datasets import make_classification

    X, y = make_classification(10000, shift=0.33, random_state=42)

    fs = FeatureSelector()
    fs.fit(X, y)
