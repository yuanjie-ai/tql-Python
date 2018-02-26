```python
class FeatureSelector(object):
    """
    from sklearn.feature_selection import SelectPercentile, SelectKBest, VarianceThreshold
    from sklearn.feature_selection import chi2, f_classif, mutual_info_classif
    from sklearn.feature_selection import f_regression, mutual_info_regression
    :param steps:
        VarianceThreshold(threshold=0.95 * (1 - 0.95))
        SelectPercentile(chi2, 90)
        SelectPercentile(mutual_info_classif, 90)
        SelectKBest(mutual_info_classif, 1000)
        ...
    """

    @staticmethod
    def filter_feature_selector(X, y, *steps):
        from sklearn.pipeline import make_pipeline
        from functools import reduce
        pipe = make_pipeline(*steps)
        pipe.fit(X, y)
        features_index = reduce(lambda x, y: x[y], [i[1].get_support(True) for i in pipe.steps])  # 被选择的特征索引
        return features_index.tolist()

    @staticmethod
    def polynomial_feature_selector(X, y, *steps, clf_percentile=10):
        """
        :param steps:
            SelectPercentile(mutual_info_classif, percentile=10)
            RandomForestClassifier()
            # LGBMClassifier(learning_rate=0.03, n_estimators=200, random_state=42, n_jobs=16)
        """
        
        from sklearn.pipeline import make_pipeline
        pipe = make_pipeline(*steps)
        pipe.fit(X, y)
        features_index = [i[1] for i in
                          sorted(zip(pipe.steps[1][1].feature_importances_, pipe.steps[0][1].get_support(True)))[::-1]]
        return features_index[:int(clf_percentile / 100 * len(features_index))]
```
