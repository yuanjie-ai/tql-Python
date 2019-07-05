#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : Text2Sequence
# @Time         : 2019-06-23 16:08
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from sklearn.base import BaseEstimator, TransformerMixin
from tensorflow.python.keras.preprocessing.sequence import pad_sequences
from ...pipe import tqdm


class Text2Sequence(BaseEstimator, TransformerMixin):

    def __init__(self, num_words=None, maxlen=128, tokenizer=str.split):
        """OOV索引为1: embedding多了两个索引0（padding）和 1（oov）

        :param num_words:
        :param maxlen:
        :param tokenizer:
        """
        self._num_words = num_words
        self._maxlen = maxlen
        self._tokenizer = tokenizer  # 必须返回list
        self.word2index = None
        self.index2word = None

    def fit(self, X):
        if self._num_words:
            _ = {}
            for doc in tqdm(X):
                for word in self._tokenizer(doc):
                    _[word] = _.get(word, 0) + 1
            _ = dict(sorted(_.items(), key=lambda x: x[1], reverse=True)[:self._num_words])

        else:
            _ = set()
            for doc in tqdm(X):
                _.update(self._tokenizer(doc))
            print('num_words: %s' % len(_))

        self.index2word = dict(enumerate(_, 2))
        self.index2word[1] = '__OOV__'
        self.word2index = {v: k for k, v in self.index2word.items()}
        return self

    def transform(self, X, padding='post', truncating='post'):
        """

        :param X: ["我是第一条文本",]
        :param padding: 前补后补
        :param truncating: 前移除后移除
        :return:
        """
        docs = map(self._tokenizer, X)
        mapper = lambda doc: [self.word2index.get(w, 1) for w in doc]
        pad_docs = pad_sequences(list(map(mapper, docs)),
                                 self._maxlen,
                                 padding=padding,
                                 truncating=truncating)
        return pad_docs
