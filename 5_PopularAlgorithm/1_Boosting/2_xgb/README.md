<h1 align = "center">:rocket: xgb常用参数 :facepunch:</h1>

---
## XGB
### 1. 原生接口
- 分类
```python
params = {
    'booster': 'gbtree', #  'dart'
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
    'nthread': -1,
    'seed': 888,
}
```
- 回归
```python
params = {
    'booster': 'gbtree', # 'dart', 'gblinear'
    'objective': 'reg:gamma',
    'gamma': 0.1,
    'max_depth': 5,
    'lambda': 3,
    'subsample': 0.7,
    'colsample_bytree': 0.7,
    'min_child_weight': 3,
    'silent': 1,
    'eta': 0.1,
    'seed': 1000,
    'nthread': 4,
}
```
---
```python
xgb_data = xgb.DMatrix(X, y)

xgb.train(params,
          dtrain,
          num_boost_round=10,
          evals=[(dtrain, 'train'), (dval, 'val')],
          
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
### 2. SK接口
- 分类
```python
clf = XGBClassifier(booster='gbtree', 
                    objective='binary:logistic', 
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
                    n_jobs=4)
```
- 回归
```python
clf.fit(X_train, y_train, 
	sample_weight=None, # 可初始化样本权重
	eval_set=[(X_train, y_train), (X_val, y_val)], 
        eval_metric='auc', 
        early_stopping_rounds=None, 
        verbose=50)
```
---
## 参数 
http://www.cnblogs.com/ljygoodgoodstudydaydayup/p/6665239.html
http://blog.csdn.net/han_xiaoyang/article/details/52665396
