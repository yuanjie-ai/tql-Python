- Auc
```python
def k_flod_cv(clf, X, y, cv=3, metrics='f1', stratified=True, seed=42):
    from sklearn.model_selection import KFold, StratifiedKFold
    from sklearn.metrics import roc_auc_score, f1_score, classification_report
    if stratified:
        kf = StratifiedKFold(cv, True, seed).split(X, y)
    else:
        kf = KFold(cv, True, seed).split(X, y)
    loss = []
    for i, (train_index, test_index) in enumerate(kf, 1):
        X_train, X_test, y_train, y_test = X[train_index], X[test_index], y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        y_pred = clf.predict_proba(X_test)[:, 1]

        if metrics == 'f1':
            threshold = sorted(y_pred)[::-1][y_test.sum()]
            y_pred = np.where(y_pred > threshold, 1, 0)

            print("%d flod:\n" % i, classification_report(y_test, y_pred))
            loss.append(f1_score(y_test, y_pred))
        else:
            loss.append(roc_auc_score(y_test, y_pred))
    print(loss)
    print("CV-Score: %0.5f (+/- %0.3f)" % (np.mean(loss), np.std(loss)))
    return loss
```
