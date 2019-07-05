#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'nms'
__author__ = 'JieYuan'
__mtime__ = '2019-05-14'
"""

import numpy as np
import nmslib
from collections import OrderedDict


class VecQuery(object):
    """
    index.getDistance
    index.knnQueryBatch
    index.loadIndex
    index.saveIndex
    """

    def __init__(self, index=None):
        """
        # TODO：index, id2word 都要存才能保证下次加载判断逻辑正确
        :param index: index.loadIndex('*')
        """
        self.id2word = {}
        self.word2id = {}
        self.index = index

    def __call__(self, *args, **kwargs):
        return self.query(*args, **kwargs)

    def query(self, data, k=10, num_threads=4):
        _ = self.index.knnQueryBatch(data, k, num_threads)
        return list(map(self._parse_result, _))

    def createIndex(self, words, vectors):
        """
        :param words: 务必唯一不重复
        :param vectors:
        :return:
        """
        if not self.id2word:
            print('Index Create ...')
            self.id2word, self.word2id = self._add(words)
            self._create(vectors)
        else:
            print('Index Add...')
            _add_ids = []
            for id, word in enumerate(words):
                if word not in self.word2id:  # 忽略已存在的索引
                    self.word2id[word] = len(self.word2id)
                    _add_ids.append(id)
            vectors = np.array(vectors)[_add_ids]
            self._create(vectors, len(self.id2word) + np.arange(len(_add_ids)))  # 增量更新索引
            self.id2word = {j: i for i, j in self.word2id.items()}

    def _add(self, words):
        id2word = dict(enumerate(words))
        word2id = {j: i for i, j in id2word.items()}
        return id2word, word2id

    def _create(self, vectors, ids=None):
        # initialize a new index, using a HNSW index on Cosine Similarity
        self.index = nmslib.init(method='hnsw', space='cosinesimil') if not self.index else self.index
        self.index.addDataPointBatch(vectors, ids)
        self.index.createIndex({'post': 2})

    def _parse_result(self, pair):
        return OrderedDict([(self.id2word[k], 1 - v) for k, v in zip(*pair)])


if __name__ == '__main__':
    vq = VecQuery()
    vq.createIndex(['a', 'b'], [[1, 2], [3, 4]])
    print(vq.query([[1, 2]]))
    print(vq.id2word, vq.word2id)
    vq.createIndex(['a', 'c'], [[1, 2], [3, 3]])

    print(vq.query([[1, 2], [1, 2]]))
    print(vq.id2word, vq.word2id)
