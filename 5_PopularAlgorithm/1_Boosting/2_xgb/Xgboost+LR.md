<h1 align = "center">:rocket: Xgboost + LR :facepunch:</h1>

---
## [Xgboost+LR][1]
- 1. [xgboost-tuner][1]
- 2. [xgbfir][2]
- 3. [xgbfi][3]
---
[1]: https://github.com/cwerner87/xgboost-tuner
[2]: https://github.com/limexp/xgbfir
[3]: https://github.com/Far0n/xgbfi

```python
import numpy as np
from sklearn import metrics
from sklearn.datasets import load_iris
from xgboost.sklearn import XGBClassifier
X = load_iris().data[:, :2]
y = load_iris().target
clf = XGBClassifier(
    n_estimators=10,
    learning_rate =0.3,
    max_depth=10,
    min_child_weight=1,
    gamma=0.3,
    subsample=0.8,
    colsample_bytree=0.8,
    objective= 'binary:logistic',
    nthread=12,
    scale_pos_weight=1,
    reg_lambda=1,
    seed=88)
```
```python
# 原始特征
model1 = clf.fit(X, y)
metrics.accuracy_score(y, model1.predict(X))
# 0.82666666666666666

# xgb组合特征生成新特征
# model_bst = xgb.train(params, d_train, 30, watchlist, early_stopping_rounds=500, verbose_eval=10)
# train_new_feature= model_bst.predict(d_train, pred_leaf=True)
_X = model1.apply(X)
model2 = clf.fit(_X, y)
metrics.accuracy_score(y, model2.predict(_X))
# 0.87333333333333329

# 原始特征+新特征
__X = np.hstack([X, _X])
model3 = clf.fit(__X, y)
metrics.accuracy_score(y, model3.predict(__X))
# 0.88
```





## [kaggle案例][2]

---
## 参照
- https://github.com/lytforgood/MachineLearningTrick
- http://blog.csdn.net/sb19931201/article/details/65445514
- http://blog.csdn.net/bryan__/article/details/51769118
---
[1]: http://nbviewer.jupyter.org/github/Jie-Yuan/2_DataMining/blob/master/5_PopularAlgorithm/1_Xgboost/XgboostAndLR/XgboostAndLR.ipynb
[2]: http://www.csie.ntu.edu.tw/~r01922136/kaggle-2014-criteo.pdf
