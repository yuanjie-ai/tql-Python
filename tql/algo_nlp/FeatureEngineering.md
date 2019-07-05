[<h1 align = "center">:rocket: NLP特征轮 :facepunch:</h1>][1]

---

- 简述：
1. 核心词特征：特征主要由词袋模型，TF-IDF特征为代表。分词算法确定特征粒度。
2. 语序特征：模板方法特征抽取，word2vec含有基于语料顺序的特征。rnn 会学习到部份语序特征。ngram会学习到字成词特征。
3. 意图特征：意图识别，通过监督方法迁移入特征。
4. 主题特征：类似意图特征
5. 其它：字型特征，拼音特征，五笔五角号码特征，字符串特征，知识图谱特征。聚类生成特征。
也流行不做特征工程基于end2end的解决方案。


https://blog.csdn.net/sinat_26917383/article/details/83584728
---
## 1. 特征工程

### 统计特征
- 长度：
    - 字
    - 词（按词性/实体）
    - 特殊符号
- BOW


- question(leak): 
  - tf: q1/q2/q1+q2
  - tfidf: q1/q2/q1+q2
  
- words(chars): 针对字符串计算
  - 词数
  - 词数差
  - 重叠词数：`len(set(q1) & set(q2))`
  - 相同度（相异度 = 1 - 相同度）: com / (q1 + q2 - com)每个状态分量根据目标设置最优权重
  - simhash
  - jaccard: `jaccard = lambda a, b: len(set(a).intersection(b))/(len(set(a).union(b))+0.)`
  - 对目标影响大的词（lstm状态差等）
  - 编辑距离
    - fuzz.QRatio
    - fuzz.WRatio
    - fuzz.partial_ratio
    - fuzz.token_set_ratio
    - fuzz.token_sort_ratio
    - fuzz.partial_token_set_ratio
    - fuzz.partial_token_sort_ratio
    - ...

  
- [doc2num][3]: 针对tf/tfidf/wordVectors等计算
  - n-grams: 结合tf/tfidf使用
  - gensim
    - wmd
    - norm_wmd(l2): norm_model.init_sims(replace=True)
  - skew/kurtosis: `from scipy.stats import skew, kurtosis`
  - scipy.spatial.distance: `import braycurtis, canberra, cityblock, cosine, euclidean, jaccard, minkowski`
  - cosine（修正）

- lda
- bleu（机器翻译指标）：对两个句子的共现词频率计算`torchtext`



---
[1]: https://github.com/binzhouchn/Algorithm_Interview_Notes-Chinese/tree/master/B-%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86
[2]: https://github.com/Jie-Yuan/text2vec
[3]: https://www.kaggle.com/kardopaska/fast-how-to-abhishek-s-features-w-o-cray-xk7
https://www.kaggle.com/rethfro/1d-cnn-single-model-score-0-14-0-16-or-0-23
