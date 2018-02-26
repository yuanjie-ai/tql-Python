
```python
class FeatureSelector(object):

    def __init__(self, *steps):
        from sklearn.pipeline import make_pipeline
        from sklearn.feature_selection import SelectPercentile, SelectKBest, VarianceThreshold
        from sklearn.feature_selection import chi2, f_classif, mutual_info_classif
        from sklearn.feature_selection import f_regression, mutual_info_regression
        """
        :param steps:
            VarianceThreshold(threshold=0.95 * (1 - 0.95))
            SelectPercentile(chi2, 90)
            SelectPercentile(mutual_info_classif, 90)
            SelectKBest(mutual_info_classif, 1000)
            ...
        """
        self.pipe = make_pipeline(*steps)

    def get_features_index(self, X, y):
        from functools import reduce

        self.pipe.fit(X, y)
        features_index = reduce(lambda x, y: x[y], [i[1].get_support(True) for i in self.pipe.steps])  # 被选择的特征索引
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
