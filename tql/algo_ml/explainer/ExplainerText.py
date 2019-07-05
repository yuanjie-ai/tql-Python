#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : ExplainNLP
# @Time         : 2019-06-20 13:24
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 

from nlp.models import BaselineBow
from sklearn.linear_model import LogisticRegression
from lime.lime_text import LimeTextExplainer


# import eli5
# from eli5.lime import TextExplainer
#
# te = TextExplainer(random_state=42)
# te.fit(doc, pipe.predict_proba)
# te.show_prediction(target_names=twenty_train.target_names)

class ExplainerText(object):
    """
    X = df.review.astype(str).map(lambda x: ' '.join(jieba.cut(x)))
    y = df.label

    enlp = ExplainNLP()
    enlp.fit(X, y)
    enlp.explain(X[0])
    """

    def __init__(self, estimator=LogisticRegression(), class_names=None):
        self._baseline = BaselineBow(estimator)()
        self._explainer = LimeTextExplainer(verbose=True, class_names=class_names)

    def fit(self, X, y):
        self._baseline.fit(X, y)
        return self._baseline

    def explain(self, sentence, num_features=6):
        """
        :param sentence: '分词 空格 拼接'
        :param num_features:
        :return:
        """
        exp = self._explainer.explain_instance(
            sentence, self._baseline.predict_proba, num_features=num_features)

        exp.show_in_notebook(text=1 if len(sentence) < 256 else 0)

        return exp
