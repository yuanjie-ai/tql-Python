<h1 align = "center">:rocket: 参数 :facepunch:</h1>

---
## [lgb][1]
```python
clf = LGBMClassifier(boosting_type='gbdt', 
                     objective='binary', # objective='multiclass', num_class = 3【多分类要指定类别数】
                     max_depth=-1,
                     num_leaves=31, 
                     learning_rate=0.1, 
                     n_estimators=10,  
                     
                     min_split_gain=0.0, 
                     min_child_weight=5, 
                     
                     subsample=1.0, 
                     subsample_freq=1, 
                     colsample_bytree=1.0, 
                     
                     reg_alpha=0.0, 
                     reg_lambda=0.0,
                     
		     scale_pos_weight=1, # is_unbalance=True 不能同时设

                     random_state=888,
                     n_jobs=4)

clf.fit(X_train, y_train, 
        eval_set=[(X_train, y_train), (X_test, y_test)], 
        eval_metric='logloss', 
        early_stopping_rounds=None, 
        verbose=50, 
        feature_name='auto', 
	categorical_feature='auto') # 只支持int类型的categorical且索引从0开始data.xx.astype('category')【参数默认即可，不告警】
```
---
## [xgb][2]
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
        eval_set=[(X_train, y_train), (X_test, y_test)], 
        eval_metric='logloss', 
        early_stopping_rounds=None, 
        verbose=50)
```

---
[1]: https://lightgbm.readthedocs.io/en/latest/Parameters.html
[2]: https://github.com/dmlc/xgboost/tree/master/demo
