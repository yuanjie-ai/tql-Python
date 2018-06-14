<h1 align = "center">:rocket: 自定义评估指标 :facepunch:</h1>

---
```python
#XGBoost
from sklearn import metrics
def gini_xgb(preds, dtrain):
    labels = dtrain.get_label()
    gini_score = gini_normalizedc(labels, preds)
    return [('gini', gini_score)]

#LightGBM
def gini_lgb(actuals, preds):
    return 'gini', gini_normalizedc(actuals, preds), True

#SKlearn
gini_sklearn = metrics.make_scorer(gini_normalizedc, True, True)
```



---
