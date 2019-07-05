#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '19-1-3'
"""
import numpy as np
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans, MeanShift
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

"""
SpectralClustering
import hdbscan 待补充 
"""


class BaselineCluster(object):
    """
    bc = BaselineCluster(X, y)
    new_X = np.column_stack((
            bc.kmeans.transform(X),
            bc.kmeans.predict(X),
            bc.mean_shift.predict(X),
            bc.gaussian_mixture.predict(X),
            bc.dbscan(),
            bc.agglomerative()
        ))
    """

    def __init__(self, X, y, random_state=None):
        self.standard_scaler = StandardScaler()
        self.X = self.standard_scaler.fit_transform(X.astype(float))
        class_weight = dict(enumerate(len(y) / (2 * np.bincount(y))))
        self.n_clusters = len(class_weight)
        self.sample_weight = [class_weight[i] for i in y]
        self.random_state = random_state

    @property
    def kmeans(self):
        """
        model.transform(X) 返回到x,y的距离
        model.predict(X) 返回类中心
        """
        model = KMeans(self.n_clusters, random_state=self.random_state, n_jobs=8)
        model.fit(self.X, sample_weight=self.sample_weight)
        return model

    @property
    def mean_shift(self):
        """
         Mean-shift（即：均值迁移）的基本思想：在数据集中选定一个点，然后以这个点为圆心，r为半径，画一个圆(二维下是圆)，
         求出这个点到所有点的向量的平均值，而圆心与向量均值的和为新的圆心，然后迭代此过程，直到满足一点的条件结束
        :return: model.predict(X) 返回类中心
        """
        model = MeanShift(n_jobs=8, bin_seeding=True)
        model.fit(self.X)
        return model

    @property
    def gaussian_mixture(self):
        """
        :return: model.predict(X) 返回类中心
        """
        model = GaussianMixture(self.n_clusters, random_state=self.random_state)
        model.fit(self.X)
        return model

    def dbscan(self):
        """
        DBSCAN（Density-Based Spatial Clustering of Application with Noise）基于密度的空间聚类算法

        model.predict(X) 返回类中心
        """
        model = DBSCAN(n_jobs=8)
        return model.fit_predict(self.X, sample_weight=self.sample_weight)

    def agglomerative(self):
        """
        Hierarchical Clustering(层次聚类)：就是按照某种方法进行层次分类，直到满足某种条件为止。
        :return: 只有结果没有模型
        """
        model = AgglomerativeClustering(self.n_clusters)
        return model.fit_predict(self.X)
