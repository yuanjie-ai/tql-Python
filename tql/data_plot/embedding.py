#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : embedding
# @Time         : 2019-07-22 11:53
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

import matplotlib.pyplot as plt
from sklearn.manifold import TSNE
from gensim.models.fasttext import load_facebook_model

fasttext = load_facebook_model('../../../fds/data/wv/skipgram.title')

word = '周杰伦'
words = [word]
words_v = [fasttext.wv[word]]
for w, _ in fasttext.wv.similar_by_word('周杰伦', 50):
    words.append(w)
    words_v.append(fasttext.wv[w])

points = TSNE().fit_transform(words_v)

plt.figure(figsize=(12, 12))  # in inches
for i in range(len(words)):
    x = words_v[i][0]
    y = words_v[i][1]
    plt.scatter(x, y)
    plt.annotate(words[i], (x, y), ha='center', va='top')
plt.show()
