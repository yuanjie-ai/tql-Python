# coding: utf-8
__title__ = 'prediction'
__author__ = 'JieYuan'
__mtime__ = '2018/2/13'

from .__init__ import *


def cv(clf, X, y, cv=3, stratified=True, seed=42):
    from sklearn.model_selection import KFold, StratifiedKFold
    from sklearn.metrics import roc_auc_score, f1_score, classification_report

    if stratified:
        kf = StratifiedKFold(cv, True, seed).split(X, y)
    else:
        kf = KFold(cv, True, seed).split(X, y)

    f1_loss = []
    auc_loss = []
    for i, (train_index, test_index) in enumerate(kf, 1):
        X_train, X_test, y_train, y_test = X[train_index], X[test_index], y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        y_pred = clf.predict_proba(X_test)[:, 1]
        auc_loss.append(roc_auc_score(y_test, y_pred))

        # threshold = sorted(y_pred)[::-1][y_test.sum()]
        # y_pred = np.where(y_pred > threshold, 1, 0)
        y_pred = get_class(y_pred, y_test.sum())
        print("%d flod:\n" % i, classification_report(y_test, y_pred))
        f1_loss.append(f1_score(y_test, y_pred))

    print(" F1-CV-Score: %0.5f (+/- %0.3f)" % (np.mean(f1_loss), np.std(f1_loss)))
    print("Auc-CV-Score: %0.5f (+/- %0.3f)" % (np.mean(auc_loss), np.std(auc_loss)))
    return f1_loss, auc_loss


def get_class(y_pred, n_pos):
    """
    :param y_pred: clf.predict_proba(X_test)[:, 1]
    :param n_pos: n Positive sample
    :return: 计算f1可用到
    """
    threshold = sorted(y_pred)[::-1][n_pos]
    y_pred = np.where(y_pred > threshold, 1, 0)
    return y_pred
