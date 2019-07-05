#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'WordVec2BOW'
__author__ = 'JieYuan'
__mtime__ = '19-3-6'
"""
from sklearn.feature_extraction.text import CountVectorizer


class WordVec2BOW(object):

    def __init__(self, wv):
        self.wv = wv  # wv = gensim.models.KeyedVectors.load_word2vec_format('./title_words.vector.bin', binary=True)
        self.cv = CountVectorizer(tokenizer=lambda x: x, lowercase=False)
        self.cv.fit([self.wv.index2word])  # wv词库务必包含corpus, 可改写为wv词库与corpus并集
        self.vocabulary = self.cv.vocabulary_

    def transform(self, corpus):
        mat = self.cv.transform(corpus).tolil().astype(float)
        for i in range(len(corpus)):
            cosine_dict = self.get_cosine_dict(corpus[i])
            word_idx = [self.vocabulary.get(w) for w in cosine_dict]
            word_value = list(cosine_dict.values())
            mat[i, word_idx] = word_value
        return mat

    def get_cosine_dict(self, sent, topn=10):
        """
        从词的角度出发考虑的，最后的效果非常好，就是怎么样从词的向量得到句子的向量。
        首先选出一个词库，比如说10万个词，然后用w2v跑出所有词的向量，然后对于每一个句子，
        构造一个10万维的向量，向量的每一维是该维对应的词和该句子中每一个词的相似度的最大值。
        """
        dic = {}
        for w in sent:
            if w in self.wv:
                _ = self.wv.similar_by_word(w, topn)
                dic.update({k: max(dic.get(k, 0), v) for k, v in _ if k not in sent})
        return dic
