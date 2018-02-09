- Auc
```python
import numpy as np
from sklearn.model_selection import KFold, StratifiedKFold
from sklearn.metrics import roc_auc_score


def k_flod_cv(clf, X, y, cv=3, stratified=True, seed=42):
    if stratified:
        kf = StratifiedKFold(cv, True, seed).split(X, y)
    else:
        kf = KFold(cv, True, seed).split(X, y)
    loss = []
    for i, (train_index, test_index) in enumerate(kf, 1):
        X_train, X_test, y_train, y_test = X[train_index], X[test_index], y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        y_pred = clf.predict_proba(X_test)[:, 1]
        loss.append(roc_auc_score(y_test, y_pred))
    print(loss)
    print("cv=%d\tAuc: %0.5f (+/- %0.3f)" % (cv, np.mean(loss), np.std(loss)))
```

- f1
```
def k_flod_cv(clf, X, y, cv=3, stratified=True, seed=42):
    if stratified:
        kf = StratifiedKFold(cv, True, seed).split(X, y)
    else:
        kf = KFold(cv, True, seed).split(X, y)
    loss = []
    for i, (train_index, test_index) in enumerate(kf, 1):
        X_train, X_test, y_train, y_test = X[train_index], X[test_index], y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        y_pred = clf.predict_proba(X_test)[:, 1]
        
        threshold = sorted(y_pred)[::-1][y_test.sum()]
        y_pred = np.where(y_pred > threshold, 1, 0)
        
        print(classification_report(y_test, y_pred))
        loss.append(f1_score(y_test, y_pred))
    print(loss)
    print("f1_score: %0.5f (+/- %0.3f)" % (np.mean(loss), np.std(loss)))
```
