#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : textcnn_fasttext
# @Time         : 2019-06-23 19:10
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from tql.pipe import *
from tql.algo_nlp.utils import Text2SequenceByFastText
from tql.algo_dl.keras.utils import DataIter
from tql.algo_dl.keras.models import TextCNN
from gensim.models.fasttext import load_facebook_model

jieba.initialize()

fasttext = load_facebook_model('../../../fds/data/wv/skipgram.title')
df = pd.read_csv('../../../fds/data/sentiment.tsv.zip', '\t')
ts = Text2SequenceByFastText(maxlen=128, fasttext_model=fasttext, tokenizer=jieba.cut)
X = ts.fit_transform(df.text.astype(str))
y = df.label

cnn = TextCNN(len(ts.word2index), maxlen=128, weights=ts.weights)(1)
cnn.compile('adam', 'binary_crossentropy', metrics=['accuracy'])
cnn.fit_generator(DataIter(X, y, batch_size=128), epochs=10)
# cnn.fit(X, y, batch_size=128, epochs=10, validation_split=0.3)
