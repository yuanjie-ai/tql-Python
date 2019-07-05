## RFE
## RFECV
```python
from lightgbm import LGBMClassifier
from sklearn.feature_selection import RFE, RFECV
from sklearn.model_selection import StratifiedKFold

skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
estimator = LGBMClassifier(learning_rate=0.03, n_estimators=200, random_state=42, n_jobs=16)
# selector = RFE(estimator, n_features_to_select=500, step=10, verbose=50)
selector = RFECV(estimator, step=10, cv=skf, scoring='roc_auc', verbose=50, n_jobs=16)
selector.fit(X, y)
```

