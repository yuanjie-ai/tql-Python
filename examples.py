#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : examples
# @Time         : 2019-06-20 14:40
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


# from keras_bert import load_trained_model_from_checkpoint, Tokenizer


import pandas as pd


df0 = pd.read_excel('./neg.xls', names=['text']).assign(label=0)
df1 = pd.read_excel('./pos.xls', names=['text']).assign(label=1)

df0.append(df1).to_csv('./sentiment.tsv', '\t', index=False)