#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'Sent2Vec'
__author__ = 'JieYuan'
__mtime__ = '19-3-1'
"""

import numpy as np
from tqdm import tqdm

"""
1. 加和/平均
2. Concatenated p-mean Word Embeddings: https://blog.csdn.net/triplemeng/article/details/81298100
3. InferSent: https://github.com/facebookresearch/InferSent
"""


class Sent2Vec(object):

    def __init__(self, gensim_model=None, fname=None):
        gensim_model.init_sims(replace=True)  # 节省内存
        self.gensim_model = gensim_model
        self.fname = fname
        self._load_wv()

    def transform(self, sentence, tokenizer=str.split, mode='mean', normalize=False):
        words = []
        flag = isinstance(self.embeddings, dict)
        for w in tokenizer(sentence.lower()):
            if flag and w in self.embeddings:
                w = self.embeddings[w]
            else:
                w = self.embeddings[w]
            words.append(w)
        if words:
            if mode in ('sum', 'mean'):
                _ = np.array(words)
                _ = _.__getattribute__(mode)(axis=0)
                return _ / np.sqrt(np.clip((_ ** 2).sum(), 1e-12, None)) if normalize else _
            else:
                return np.zeros(self.word_size)
        else:
            return np.zeros(self.word_size)

    def _load_wv(self):
        if self.fname is None and self.gensim_model is None:
            raise Exception('fname and gensim_model can not be both None!')

        if self.gensim_model:
            self.word_size = self.gensim_model.wv.vector_size
            self.embeddings = self.gensim_model.wv

        if self.fname:
            with open(self.fname) as f:
                for line in tqdm(f, 'Load Vectors ...'):
                    line = line.strip().split()
                    if len(line) > 2:
                        self.embeddings[line[0]] = np.asarray(line[1:], dtype='float32')
                self.word_size = len(line[1:])
