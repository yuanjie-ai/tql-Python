```python
import warnings

warnings.filterwarnings('ignore')
from udfs import *
from bayes_opt import BayesianOptimization
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import cross_val_score

class BayesOpt(object):
    def __init__(self):
        pass

    @staticmethod
    def rf():
        BoParams = {
            'n_estimators': (120, 1200),
            'max_depth': (6, 30),
            'min_samples_split': (1, 100),
            'min_samples_leaf': (1, 10),
        }
        BO = BayesianOptimization(_rf_loss, BoParams)
        BO.maximize(init_points=5, n_iter=10, acq='ucb', kappa=2.576, xi=0.0)
        print(BO.res['max'])
        return BO.res

    @staticmethod
    def lr():
        BoParams = {
            'n_estimators': (120, 1200),
            'max_depth': (6, 30),
            'min_samples_split': (1, 100),
            'min_samples_leaf': (1, 10),
        }
        BO = BayesianOptimization(_rf_loss, BoParams)
        BO.maximize(init_points=5, n_iter=10, acq='ucb', kappa=2.576, xi=0.0)
        print(BO.res['max'])
        return BO.res


def _lr_loss(n_estimators, max_depth, min_samples_split, min_samples_leaf):
    clf = RandomForestClassifier(n_estimators=int(n_estimators),
                                 max_depth=int(max_depth),  # 5, 8, 15, 25, 30
                                 criterion='gini',  # 'entropy'
                                 min_samples_split=int(min_samples_split),  # 1, 2, 5, 10, 15, 100
                                 min_samples_leaf=int(min_samples_leaf),  # 1, 2, 5, 10
                                 max_features='auto',  # 'sqrt'
                                 n_jobs=4,
                                 random_state=42)
    scores = cross_val_score(clf, X, y, cv=3, scoring='roc_auc')
    return scores.mean()

def _rf_loss(n_estimators, max_depth, min_samples_split, min_samples_leaf):
    clf = RandomForestClassifier(n_estimators=int(n_estimators),
                                 max_depth=int(max_depth),  # 5, 8, 15, 25, 30
                                 criterion='gini',  # 'entropy'
                                 min_samples_split=int(min_samples_split),  # 1, 2, 5, 10, 15, 100
                                 min_samples_leaf=int(min_samples_leaf),  # 1, 2, 5, 10
                                 max_features='auto',  # 'sqrt'
                                 n_jobs=4,
                                 random_state=42)
    scores = cross_val_score(clf, X, y, cv=3, scoring='roc_auc')
    return scores.mean()
```
