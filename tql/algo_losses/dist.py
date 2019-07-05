#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'dist'
__author__ = 'JieYuan'
__mtime__ = '2019-05-24'
"""
from scipy.spatial.distance import pdist
from functools import partial

from scipy.spatial.distance import pdist
from functools import partial


class Distance(object):

    def __init__(self, metric='cosine'):
        if metric in self.metrics:
            for metric in self.metrics:
                func = partial(pdist, metric=metric)
                setattr(self, metric, func)

    @property
    def metrics(self):
        _ = ['cosine',
             'euclidean',
             'jaccard',
             'cityblock',
             'braycurtis',
             'canberra',
             'chebyshev',
             'correlation',
             'dice',
             'hamming',
             'jensenshannon',
             'kulsinski',
             'mahalanobis',
             'matching',
             'minkowski',
             'rogerstanimoto',
             'russellrao',
             'seuclidean',
             'sokalmichener',
             'sokalsneath',
             'sqeuclidean',
             'yule']
        return _
