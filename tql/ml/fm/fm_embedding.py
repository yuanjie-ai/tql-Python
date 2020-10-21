#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : fm_embedding
# @Time         : 2020/10/9 8:19 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

import numpy as np
from lightfm import LightFM

from scipy.sparse import csr_matrix


class FMEmbedding(object):

    def __init__(self, dim=128, **kwargs):
        self.fm = LightFM(no_components=dim, random_state=666, **kwargs)

    def fit(self, df, epochs=10, num_threads=30, verbose=True):
        """

        :param df: ['uid', 'iid', 'rating']
        :return:
        """
        df.columns = ['uid', 'iid', 'rating']
        csr_data = csr_matrix((df['rating'], (df['uid'], df['iid'])))

        print(f"csr_data: {csr_data.shape}")

        self.fm.fit(csr_data, epochs=epochs, num_threads=num_threads, verbose=verbose)

        self.user_embeddings = np.ascontiguousarray(self.fm.user_embeddings)
        self.item_embeddings = np.ascontiguousarray(self.fm.item_embeddings)

# if __name__ == '__main__':
#     import faiss
#     from ann import ANNFaiss
#
#     ann = ANNFaiss()
#
#     ann.train(item_embeddings, index_factory='IVF4000, Flat', metric=faiss.METRIC_INNER_PRODUCT, noramlize=True)
#
#     ann.noramlize()
