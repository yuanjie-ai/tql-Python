```
import gensim
# datatype=np.float 最快
# datatype=np.float 最省内存
model = gensim.models.KeyedVectors.load_word2vec_format('./Tencent_AILab_ChineseEmbedding.txt', datatype=np.float)
```

[无监督词向量][1]

```python
# 计算两个词的相似度
model.wv.similarity('周杰伦', '周董啊') 
model.wv.similarity('何超盈拍孕肚写真', '奚梦瑶疑似怀孕')
# 词集合 相似度
model.wv.n_similarity('何超盈拍孕肚写真' | xcut, '奚梦瑶疑似怀孕' | xcut)
# 相似词
model.wv.similar_by_word('怀孕', topn=3)

# 一对多向量相似度
# 一对多词找最相似
model.wv.cosine_similarities(model['周杰伦'], [model['周杰伦'], model['周杰伦']])
model.wv.most_similar_to_given('周杰伦', ['周杰伦', '周董'])


# 增强版 最相似的词
model.wv.most_similar(['男人'], ['女人'])
model.wv.most_similar_cosmul(['男人'], ['女人'])
model.wv.similar_by_vector(model['男人'] - model['女人'])

model.wv.most_similar_cosmul(positive=['苹果手机'], negative=['手机'], topn=10)
model.wv.most_similar(positive=['苹果手机'], negative=['手机'], topn=10)
model.wv.similar_by_vector(model['苹果手机'] - model['手机'])

# 异类
model.wv.doesnt_match(['周杰伦', '周董', '林俊杰'])

##?
model.wv.relative_cosine_similarity('周杰伦', '周杰伦')
```






---
[1]: https://x-algo.cn/index.php/2018/11/12/3083/