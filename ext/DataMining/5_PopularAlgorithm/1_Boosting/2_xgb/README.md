<h1 align = "center">:rocket: xgb常用参数 :facepunch:</h1>

---
## 1. 原生接口
- 分类
```python
"""
max_delta_step: 类别不平衡有助于逻辑回归
"""
params = {
    'booster': 'gbtree', #  'dart' # 'rank:pairwise'对排序友好
    'objective': 'binary:logistic', # 'objective': 'multi:softmax', 'num_class': 3,
    'eta': 0.1,
    'max_depth': 7,

    'gamma': 0,
    'min_child_weight': 1,

    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'alpha': 0,
    'lambda': 1,

    'scale_pos_weight': 1,
    'eval_metric': 'auc',
    'nthread': 16,
    'seed': 888,
}
```
- 回归
```python
params = {
    'booster': 'gbtree', # 'dart', 'gblinear' 
    'objective': 'reg:linear', # 'reg:tweedie', 'reg:gamma'
    'eta': 0.1,
    'max_depth': 7,

    'gamma': 0,
    'min_child_weight': 1,

    'subsample': 0.8,
    'colsample_bytree': 0.8,
    'alpha': 0,
    'lambda': 1,

    'scale_pos_weight': 1,
    'eval_metric': 'rmse',
    'nthread': 16,
    'seed': 888
}
```

---
```python
xgb_data = xgb.DMatrix(X, y)

xgb.cv(
    params,
    xgb_data,
    num_boost_round=2000,
    nfold=3,
    stratified=True, # stratified=False # 回归
    metrics=(),
    early_stopping_rounds=50,
    verbose_eval=50,
    show_stdv=True,
    seed=0
)
       
xgb.train(
    params,
    dtrain,
    num_boost_round=2000,
    evals=[(dtrain, 'train'), (dval, 'val')],
    early_stopping_rounds=50,
    verbose_eval=50
)
```

---
## 2. SK接口
- 分类
```python
clf = XGBClassifier(
    booster='gbtree', #  'dart' # 'rank:pairwise'对排序友好
    objective='binary:logistic',  # 'multi:softmax', 
    max_depth=7,
    learning_rate=0.1,
    n_estimators=100,

    gamma=0,
    min_child_weight=1,

    subsample=1,
    colsample_bytree=1,
    colsample_bylevel=1,

    reg_alpha=0,
    reg_lambda=1,

    scale_pos_weight=1,

    random_state=888,
    n_jobs=-1
)
```
- 回归
```python
clf = XGBRegressor(
    booster='gbtree', # 'dart', 'gblinear' 
    objective='reg:linear', # 'reg:tweedie', 'reg:gamma'
    max_depth=7,
    learning_rate=0.1,
    n_estimators=100,

    gamma=0,
    min_child_weight=1,

    subsample=1,
    colsample_bytree=1,
    colsample_bylevel=1,

    reg_alpha=0,
    reg_lambda=1,

    scale_pos_weight=1,

    random_state=888,
    n_jobs=-1
)
```
---
```python
clf.fit(
    X_train, 
    y_train,
    sample_weight=None,  # 可初始化样本权重
    eval_set=[(X_train, y_train), (X_val, y_val)],
    eval_metric='auc',
    early_stopping_rounds=None,
    verbose=50
)
```
---
## 参数 
http://www.cnblogs.com/ljygoodgoodstudydaydayup/p/6665239.html
http://blog.csdn.net/han_xiaoyang/article/details/52665396
