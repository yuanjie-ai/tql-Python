`⁰ ¹ ² ³ ⁴ ⁵ ⁶ ⁷ ⁸ ⁹`
---
http://wecatch.me/markdown-css/#themes
http://htmlpreview.github.io/
---
[ELMO][1]
---
```
top10_sellers = data.pivot_table(values='Purchase',index=['Product_ID'], aggfunc='count').reset_index().sort_values(by = 'Purchase',ascending=False).head(10)

from mlxtend.frequent_patterns import apriori, association_rules
df = pd.DataFrame([[1, 1], [1, 0]], columns=['a', 'b'])
association_rules(apriori(df))

https://www.kesci.com/home/project/5be7e948954d6e0010632ef2
```

```
# 基于tf-idf特征，使用xgboost
clf = xgb.XGBClassifier(max_depth=7, n_estimators=200, colsample_bytree=0.8, 
                        subsample=0.8, nthread=10, learning_rate=0.1)
clf.fit(xtrain_tfv.tocsc(), ytrain)
predictions = clf.predict_proba(xvalid_tfv.tocsc())

    CHAR_DICT = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 .!?:,\'%-\(\)/$|&;[]"'

```

```
Runtime tricks
We aimed at combining as many models as possible. To do this, we needed to improve runtime and the most important thing to achieve this was the following. We do not pad sequences to the same length based on the whole data, but just on a batch level. That means we conduct padding and truncation on the data generator level for each batch separately, so that length of the sentences in a batch can vary in size. Additionally, we further improved this by not truncating based on the length of the longest sequence in the batch, but based on the 95% percentile of lengths within the sequence. This improved runtime heavily and kept accuracy quite robust on single model level, and improved it by being able to average more models.


 length of the text, number of capital letters, number of exclamation/question/punctuation marks, number of special symbols, number of smileys, number of words, number of unique words and few derivatives.
 
 Statistical features
the number of words
the number of unique words
the number of characters
the number of upper characters
Bag of characters: Implemented by CountVectorizer(ngram_range=(1, 1), min_df=1e-4, token_pattern=r'\w+',analyzer='char')

```

```
Statistical features
the number of words
the number of unique words
the number of characters
the number of upper characters
Bag of characters: Implemented by CountVectorizer(ngram_range=(1, 1), min_df=1e-4, token_pattern=r'\w+',analyzer='char')

https://blog.csdn.net/IT_bigstone/article/details/80739807
```

[1]: https://blog.csdn.net/sinat_26917383/article/details/81913790


# 翻译
`https://www.cnblogs.com/fanyang1/p/9414088.html`
https://github.com/Jie-Yuan/DataMining/tree/master/0_DA/udfs
https://www.kaggle.com/c/quora-insincere-questions-classification/discussion/79824
