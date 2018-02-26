
```python
from sklearn.feature_selection import SelectPercentile, VarianceThreshold
from sklearn.feature_selection import chi2, mutual_info_classif
from sklearn.pipeline import make_pipeline


class FeatureSelector(object):
    def __init__(self, threshold1=0.95, threshold2=90, threshold3=90):
        self.threshold1 = threshold1
        self.threshold2 = threshold2
        self.threshold3 = threshold3

    def get_features_index(self, X, y):
        from functools import reduce

        step1 = VarianceThreshold(threshold=self.threshold1 * (1 - self.threshold1))
        step2 = SelectPercentile(chi2, self.threshold2)
        step3 = SelectPercentile(mutual_info_classif, self.threshold3)
        pipe = make_pipeline(step1, step2, step3)
        pipe.fit(X, y)
        features_index = reduce(lambda x, y: x[y], [i[1].get_support(True) for i in pipe.steps]) # 被选择的特征索引
        return features_index
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
