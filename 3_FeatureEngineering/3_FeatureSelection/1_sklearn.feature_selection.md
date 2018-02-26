- 过滤式
  - 去除低方差的特征
```python
from sklearn.feature_selection import VarianceThreshold
selector = VarianceThreshold(threshold=0.95*(1-0.95)) # 一般不太会有95%以上都取某个值的特征存在(假如是二项分布p*(1-p))
selector.fit_transform(X, y)
```


---
```python
sklearn.feature_selection.GenericUnivariateSelect
sklearn.feature_selection.RFE
sklearn.feature_selection.RFECV
sklearn.feature_selection.SelectFdr
sklearn.feature_selection.SelectFpr
sklearn.feature_selection.SelectFromModel
sklearn.feature_selection.SelectFwe
sklearn.feature_selection.SelectKBest
sklearn.feature_selection.SelectPercentile
sklearn.feature_selection.VarianceThreshold
```
---
https://www.kaggle.com/tilii7/recursive-feature-elimination

https://www.cnblogs.com/stevenlk/p/6543628.html
