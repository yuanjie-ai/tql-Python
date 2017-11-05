<h1 align = "center">:rocket: 提升算法 :facepunch:</h1>

---
## 常用参数速查
|[**xgb**][1]|[**lgb**][2]|**xgb.sklearn**|**lgb.sklearn**|
|:--|:--|:--|:--|
|booster='gbtree'|boosting='gbdt'|booster='gbtree'|boosting_type='gbdt'|
|objective='binary:logistic'|application='binary'|objective='binary:logistic'|objective='binary'|
|max_depth=7|num_leaves=2**7|max_depth=7|num_leaves=2**7|
|eta=0.1|learning_rate=0.1|learning_rate=0.1|learning_rate=0.1|
|num_boost_round=10|num_boost_round=10|n_estimators=10|n_estimators=10|
|gamma=0|min_split_gain=0.0|gamma=0|min_split_gain=0.0|
|min_child_weight=5|min_child_weight=5|min_child_weight=5|min_child_weight=5|
|subsample=1|bagging_fraction=1|subsample=1.0|subsample=1.0|
|colsample_bytree=1.0|feature_fraction=1|colsample_bytree=1.0|colsample_bytree=1.0|
|alpha=0|lambda_l1=0|reg_alpha=0.0|reg_alpha=0.0|
|lambda=1|lambda_l2=0|reg_lambda=1|reg_lambda=0.0|
|scale_pos_weight=1|scale_pos_weight=1|scale_pos_weight=1|scale_pos_weight=1|
|seed |bagging_seed<br/>feature_fraction_seed|random_state=888|random_state=888|
|nthread|num_threads|n_jobs=4|n_jobs=4|
|||||
|evals|valid_sets|eval_set|eval_set|
|eval_metric|metric|eval_metric|eval_metric|
|early_stopping_rounds|early_stopping_rounds|early_stopping_rounds|early_stopping_rounds|
|verbose_eval|verbose_eval|verbose|verbose|

---
[1]: http://xgboost.readthedocs.io/en/latest/parameter.html#
[2]: https://lightgbm.readthedocs.io/en/latest/Parameters.html#
[3]: https://github.com/Microsoft/LightGBM/blob/master/docs/Parameters.rst
