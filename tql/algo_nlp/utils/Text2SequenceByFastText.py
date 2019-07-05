#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : EmbeddingFastText
# @Time         : 2019-06-23 17:28
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from ...pipe import tqdm


class Text2SequenceByFastText(BaseEstimator, TransformerMixin):
    """
    word2id['<PAD>'] = 0
    word2id['<START>'] = 1
    word2id['<UNK>'] = 2
    word2id['<UNUSED>'] = 3
    """

    def __init__(self, maxlen=128, fasttext_model=None, tokenizer=str.split):
        """

        :param maxlen:
        :param fasttext_model: from gensim.models.fasttext import load_facebook_model
        :param tokenizer: 必须返回列表
        """
        self.maxlen = maxlen
        self.model = fasttext_model
        self._tokenizer = tokenizer
        self.word2index = None
        self.weights = None

    def fit(self, X):
        """数据转换的过程中得到embedding的weights
        :param X:
        :return:
        """
        index2word = dict(enumerate(['__PAD__', '__OOV__'] + self.model.wv.index2entity))
        self.word2index = {v: k for k, v in index2word.items()}

        self.weights = self.model.wv.vectors
        rand_vecs = np.random.normal(size=(2, self.weights.shape[1]))  # padding/oov
        self.weights = np.row_stack((rand_vecs, self.weights))

        _array = []
        for doc in tqdm(X):
            for w in self._tokenizer(doc):
                if w not in self.word2index:
                    self.word2index[w] = len(self.word2index)
                    _array.append(self.model.wv[w])  # TODO: 非fasttext怎么解决OOV? 直接补位1（OOV标识）
        print("New Words: %s" % len(_array))

        self.weights = np.row_stack((self.weights, *_array))
        return self

    def transform(self, X, padding='post', truncating='post'):
        """

        :param X:
        :param padding: 前补后补
        :param truncating: 前移除后移除
        :return:
        """
        docs = map(self._tokenizer, X)
        mapper = lambda doc: [self.word2index.get(w, 1) for w in doc]  # 1: __OOV__
        pad_docs = pad_sequences(list(map(mapper, docs)),
                                 self.maxlen,
                                 padding=padding,
                                 truncating=truncating)
        return pad_docs
