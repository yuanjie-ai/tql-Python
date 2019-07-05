#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'rte'
__author__ = 'JieYuan'
__mtime__ = '19-1-3'
"""


class EmbeddingTrees(object):

    def embedding_random_trees(self, random_state):
        from sklearn.ensemble import RandomTreesEmbedding
        rte = RandomTreesEmbedding(
            n_estimators=256,
            max_depth=7,
            min_samples_split=2,
            min_samples_leaf=1,
            min_weight_fraction_leaf=0.0,
            max_leaf_nodes=None,
            min_impurity_decrease=0.0,
            min_impurity_split=None,
            sparse_output=True,
            n_jobs=8,
            random_state=random_state)
        return rte

