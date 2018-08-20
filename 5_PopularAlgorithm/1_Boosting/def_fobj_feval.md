<h1 align = "center">:rocket: 自定义目标/评估函数 :facepunch:</h1>

---
## 自定义函数装饰器
```python
import functools
import numpy as np


def feval(multiclass=None, is_bigger_better=True, model='lgb'):
    """example
    @feval(3)
    def f1_score(y_pred, y_true):
        '注意入参顺序'
        return f1_score(y_true, y_pred, average='macro')
    """

    @wrapt.decorator
    def wrapper(wrapped, instance, args, kwargs):
        y_pred, y_true = args
        y_true = y_true.get_label()
        if model == 'lgb':
            if multiclass:
                y_pred = np.array(y_pred).reshape(multiclass, -1).argmax(0)
            return wrapped.__name__, wrapped(y_pred, y_true), is_bigger_better
        elif is_bigger_better:
            """xgb评估指标默认越小越好"""
            return '-' + wrapped.__name__, - wrapped(y_pred, y_true)
        else:
            return wrapped.__name__, wrapped(y_pred, y_true)

    return wrapper
```

---
## Xgb

```python
def feval(y_pred, y_true):
    from ml_metrics import auc
    y_true = y_true.get_label()
    return '-auc', - auc(y_true, y_pred)
    
XGBClassifier().fit(X, y, eval_metric=feval) # 满足目标最小化
xgb.train(feval=feval, maximize=False) # 目标最大化可选
xgb.cv(feval=feval, maximize=False) # 目标最大化可选
```

---
## Lgb
```python
def feval(y_pred, y_true):
    from ml_metrics import auc
    y_true = y_true.get_label()
    return 'auc', auc(y_true, y_pred), True# maximize=False比xgb多返回一项
    
# 多分类
from sklearn.metricse import f1_score

def lgb_f1(y_pred, y_true):
    y_true = y_true.get_label()
    num_class = len(set(y_true))
    y_pred = np.array(y_pred).reshape(num_class, -1).argmax(0)
    
    score = f1_score(y_true, y_pred, average='macro')
    return 'f1_score', score, True
    
# LGBMClassifier().fit(X, y,eval_metric=feval) # 待实验
lgb.train(feval=feval)
lgb.cv(feval=feval)
```

---
##
```python
from sklearn.metrics import make_scorer
from sklearn.model_selection import cross_val_score
cross_val_score(scoring) # 自定义评估函数需要make_scorer包装一下
```
---
https://www.cnblogs.com/silence-gtx/p/5812012.html
