<h1 align = "center">:rocket: lgb常用参数 :facepunch:</h1>

---
## 1. 原生接口
- 分类
```python
params = {
    'boosting': 'gbdt', # 'rf', 'dart', 'goss'
    'application': 'binary', # 'application': 'multiclass', 'num_class': 3, # multiclass=softmax, multiclassova=ova  One-vs-All
    'learning_rate': 0.01,
    'max_depth': -1,
    'num_leaves': 2 ** 7 - 1,

    'min_split_gain': 0,
    'min_child_weight': 1,

    'bagging_fraction': 0.8,
    'feature_fraction': 0.8,
    'lambda_l1': 0,
    'lambda_l2': 1,

    'scale_pos_weight': 1,
    'metric': 'auc',
    'num_threads': 32,
}
```

- 回归
```python
params = {
    'boosting': 'gbdt', # 'rf', 'dart', 'goss'
    'application': 'regression',
    'learning_rate': 0.01,
    'max_depth': -1,
    'num_leaves': 2 ** 7 - 1,

    'min_split_gain': 0,
    'min_child_weight': 1,

    'bagging_fraction': 0.8,
    'feature_fraction': 0.8,
    'lambda_l1': 0,
    'lambda_l2': 1,

    'scale_pos_weight': 1,
    'metric': 'rmse',
    'num_threads': 32,
}
```

---
```python
lgb_data = lgb.Dataset(X, y)

lgb.cv(
    params,
    lgb_data,
    num_boost_round=2000,
    nfold=5,
    stratified=False, # 回归一定是False
    metrics=None,
    early_stopping_rounds=50,
    verbose_eval=50,
    show_stdv=True,
    seed=0
)
       
lgb.train(
    params,
    lgb_data,
    num_boost_round=2000,
    valid_sets=None,
    early_stopping_rounds=50,
    verbose_eval=50
)
```
---
## 2. SK接口
- 分类
```python
clf = LGBMClassifier(
    boosting_type='gbdt',  # 'rf', 'dart', 'goss'
    objective='binary',  # objective='multiclass', num_class = 3
    max_depth=-1,
    num_leaves=2 ** 7 - 1,
    learning_rate=0.01,
    n_estimators=1000,

    min_split_gain=0.0,
    min_child_weight=0.001,

    subsample=0.8,
    subsample_freq=1,
    colsample_bytree=0.8,

    reg_alpha=0.0,
    reg_lambda=0.0,

    scale_pos_weight=1,  # is_unbalance=True 不能同时设

    random_state=888,
    n_jobs=-1
)

```

- 回归
```python
clf = LGBMRegressor(
    boosting_type='gbdt',  # 'rf', 'dart', 'goss'
    objective='regression',
    max_depth=-1,
    num_leaves=2 ** 7 - 1,
    learning_rate=0.01,
    n_estimators=1000,

    min_split_gain=0.0,
    min_child_weight=0.001,

    subsample=0.8,
    subsample_freq=1,
    colsample_bytree=0.8,

    reg_alpha=0.0,
    reg_lambda=0.0,

    scale_pos_weight=1,  # is_unbalance=True 不能同时设

    random_state=888,
    n_jobs=-1
)

```

---
```python
clf.fit(
    X_train,
    y_train,
    eval_set=[(X_train, y_train), (X_test, y_test)],
    eval_metric='logloss',
    early_stopping_rounds=100,
    verbose=50,
    feature_name='auto',
    categorical_feature='auto'
)
```
---
