#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : textcnn
# @Time         : 2019-06-23 19:16
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  :

"""
https://m.imooc.com/article/30122读大数据
https://blog.csdn.net/lujiandong1/article/details/54869170
https://blog.csdn.net/foreseerwang/article/details/80572182
"""
import tensorflow as tf
from tql.pipe import *
from tql.algo_nlp.utils import Text2Sequence
from tql.algo_dl.keras.utils import DataIter
from tql.algo_dl.keras.models import TextCNN, TextFast

jieba.initialize()

df = pd.read_csv('../../../fds/data/sentiment.tsv.zip', '\t')
ts = Text2Sequence(num_words=None, maxlen=128, tokenizer=jieba.cut)
X = ts.fit_transform(df.text.astype(str))
y = df.label

cnn = TextCNN(len(ts.word2index) + 1, maxlen=128, embedding_size=64)(1)
cnn.compile('adam', 'binary_crossentropy', metrics=['accuracy', tf.metrics.AUC()])
cnn.fit_generator(DataIter(X, y, batch_size=128), epochs=10)
# cnn.fit(X, y, batch_size=128, epochs=10, validation_split=0.3)
