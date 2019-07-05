# AutoML

### H2O
`https://github.com/h2oai/h2o-tutorials/tree/master/h2o-world-2017/automl`
```python
from h2o.estimators.xgboost import H2OXGBoostEstimator
# http://docs.h2o.ai/h2o/latest-stable/h2o-docs/data-science/xgboost.html
xgb = H2OXGBoostEstimator(backend="gpu", 
                          learn_rate=0.01, 
                          nfolds=5, 
                          ntrees=500) # max_runtime_secs
xgb.train(x = x, y = y,
          training_frame = train)
```