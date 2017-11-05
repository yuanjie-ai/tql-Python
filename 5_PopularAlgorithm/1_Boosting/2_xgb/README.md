<h1 align = "center">:rocket: xgb常用参数 :facepunch:</h1>

---
## xgb
```python
params = {
    'booster': 'gbtree',
    'objective': 'binary:logistic',
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
    'verbose_eval': 10,
    'nthread': -1,
    'seed': 888,
    'missing': -888
}

xgb.train(params,
          dtrain,
          num_boost_round=10,
          evals=(),
          
          feval=None,
          maximize=False,

          early_stopping_rounds=None,
          verbose_eval=True)

xgb.cv(params,
       dtrain,
       num_boost_round=10,

       nfold=3,
       stratified=False,

       metrics=(),
       feval=None,
       maximize=False,

       early_stopping_rounds=None,
       verbose_eval=None,
       show_stdv=True,
       seed=0)
```
---
## xgb.sklearn
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
