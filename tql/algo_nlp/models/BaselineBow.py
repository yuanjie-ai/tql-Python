#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : tfidf_lr
# @Time         : 2019-06-20 12:02
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer


class BaselineBow(object):
    """
    from sklearn.naive_bayes import MultinomialNB
    from sklearn.linear_model import SGDClassifier
    from sklearn.linear_model import LogisticRegression
    mnb = MultinomialNB()
    svm = SGDClassifier(loss='hinge', n_iter=100)
    lr = LogisticRegression()
    """

    def __init__(self, estimator=LogisticRegression(), tokenizer=None, vectorizer=None):
        self._estimator = estimator
        self._vectorizer = vectorizer if vectorizer else TfidfVectorizer()
        self._vectorizer.tokenizer = tokenizer

    def __call__(self, *args, **kwargs):
        return self._pipline

    @property
    def _pipline(self):
        return make_pipeline(self._vectorizer, self._estimator)
