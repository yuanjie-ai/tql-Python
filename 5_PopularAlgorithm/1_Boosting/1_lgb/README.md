<h1 align = "center">:rocket: lgb常用参数 :facepunch:</h1>

---
## lgb
```python
params = {
    'boosting': 'gbdt',
    'application': 'binary',
    'learning_rate': 0.1,
    'max_depth': -1,
    'num_leaves': 2 ** 7,

    'min_split_gain': 0,
    'min_child_weight': 1,

    'bagging_fraction': 0.8,
    'feature_fraction': 0.8,
    'lambda_l1': 0,
    'lambda_l2': 1,

    'scale_pos_weight': 1,
    'metric': 'auc',
    'verbose_eval': 10,
    'num_threads': -1,
}

lgb.train(params,
          train_set,
          num_boost_round=100,
          valid_sets=None,

          feval=None,

          early_stopping_rounds=None,
          verbose_eval=True)

lgb.cv(params,
       train_set,
       num_boost_round=10,

       nfold=5,
       stratified=True,

       metrics=None,
       feval=None,

       early_stopping_rounds=None,
       verbose_eval=None,
       show_stdv=True,
       seed=0)
```

## lgb.sklearn
```python
clf = XGBClassifier(booster='gbtree', 
                    objective='binary:logistic', 
                    max_depth=3, 
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
                    n_jobs=4)

clf.fit(X_train, y_train, 
        eval_set=[(X_train, y_train), (X_val, y_val)], 
        eval_metric='auc', 
        early_stopping_rounds=None, 
        verbose=50)
```
