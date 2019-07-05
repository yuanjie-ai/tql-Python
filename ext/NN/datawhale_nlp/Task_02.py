# encoding: utf-8
from xplan.pipe import *
from xplan.nlp.utils import *

corpus = "深度学习的概念由Hinton等人于2006年提出。基于深度置信网络(DBN)提出非监督贪心逐层训练算法，为解决深层结构相关的优化难题带来希望，随后提出多层自动编码器深层结构。此外Lecun等人提出的卷积神经网络是第一个真正多层结构学习算法，它利用空间相对关系减少参数数目以提高训练性能。"

# 统计字/词频
corpus | xcount | xprint
corpus | xcut | xcount | xprint
print(corpus | xcut | xvalue_counts)

# ngrams
corpus = ['我', '喜欢', '学习', '，', '但', '成绩', '不好']
ngrams(corpus, 1) | xlist | xprint
ngrams(corpus, 2) | xlist | xprint
ngrams(corpus, 3) | xlist | xprint
everygrams(corpus, max_len=3) | xlist | xprint

# bow
doc = ['some thing to do', 'some thing to drink']
bow = BOW(num_words=20000, maxlen=8)
bow.fit(doc)
print(bow.transform(doc))
bow.word_index | xprint
