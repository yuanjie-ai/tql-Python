<h1 align = "center">:rocket: lgb常用参数 :facepunch:</h1>

---
## 1. 原生接口
- 分类
```python
params = {
    'boosting': 'gbdt',
    'application': 'binary',
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
    'num_threads': -1,
}
```
- 回归
```python
params = {
    'boosting': 'gbdt',
    'application': 'binary',
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
    'num_threads': -1,
}
```
```python
train_set = lgb.Dataset(X, y)

lgb.train(params,
          train_set,
          num_boost_round=2000,
          valid_sets=None,

          feval=None,

          early_stopping_rounds=20,
          verbose_eval=50)

lgb.cv(params,
       train_set,
       num_boost_round=2000,

       nfold=5,
       stratified=True,

       metrics=None,
       feval=None,

       early_stopping_rounds=20,
       verbose_eval=50,
       show_stdv=True,
       seed=0)
```
---
## lgb.sklearn
```python
clf = LGBMClassifier(boosting_type='gbdt', 
                     objective='binary', # objective='multiclass', num_class = 3【多分类要指定类别数】
                     max_depth=-1,
                     num_leaves=2**6, 
                     learning_rate=0.1, 
                     n_estimators=1000,  
                     
                     min_split_gain=0.0, 
                     min_child_weight=5, 
                     
                     subsample=1.0, 
                     subsample_freq=1, 
                     colsample_bytree=1.0, 
                     
                     reg_alpha=0.0, 
                     reg_lambda=0.0,
                     
                     scale_pos_weight=1, # is_unbalance=True 不能同时设

                     random_state=888,
                     n_jobs=-1)

clf.fit(X_train, y_train, 
	sample_weight=None, # 可初始化样本权重
        eval_set=[(X_train, y_train), (X_test, y_test)], 
        eval_metric='logloss', 
        early_stopping_rounds=100, 
        verbose=50, 
        feature_name='auto', 
        categorical_feature='auto') # 只支持int类型的categorical且索引从0开始data.xx.astype('category')【参数默认即可，不告警】
```
