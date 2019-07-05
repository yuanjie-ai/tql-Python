# encoding: utf-8

"""
https://blog.csdn.net/u013710265/article/details/73480332
https://blog.csdn.net/Kaiyuan_sjtu/article/details/83572927
"""
"""
LDA（Latent Dirichlet Allocation）是一种文档主题生成模型，也称为一个三层贝叶斯概率模型，包含词、主题和文档三层结构。所谓生成模型，就是说，我们认为一篇文章的每个词都是通过“以一定概率选择了某个主题，并从这个主题中以一定概率选择某个词语”这样一个过程得到。文档到主题服从多项式分布，主题到词服从多项式分布。

LDA是一种非监督机器学习技术，可以用来识别大规模文档集（document collection）或语料库（corpus）中潜藏的主题信息。它采用了词袋（bag of words）的方法，这种方法将每一篇文档视为一个词频向量，从而将文本信息转化为了易于建模的数字信息。但是词袋方法没有考虑词与词之间的顺序，这简化了问题的复杂性，同时也为模型的改进提供了契机。每一篇文档代表了一些主题所构成的一个概率分布，而每一个主题又代表了很多单词所构成的一个概率分布。

"""
from xplan import *
from xplan.models import OOF

import pandas as pd

from sklearn.naive_bayes import GaussianNB

train = pd.read_csv('train.csv', lineterminator='\n')
test = pd.read_csv('test.csv', lineterminator='\n')

y = train.label.replace({'Positive': 1, 'Negative': 0})
data = train.append(test).drop('label', 1)

