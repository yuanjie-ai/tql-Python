#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'rf'
__author__ = 'JieYuan'
__mtime__ = '19-1-2'
"""

from sklearn.ensemble import ExtraTreesClassifier, RandomForestClassifier, GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression


clf1 = ExtraTreesClassifier(
    256, n_jobs=8, class_weight='balanced', random_state=None)
clf2 = RandomForestClassifier(
    256,
    criterion='gini',
    n_jobs=8,
    class_weight='balanced',
    random_state=None)
clf3 = RandomForestClassifier(
    256,
    criterion='entropy',
    n_jobs=8,
    class_weight='balanced',
    random_state=None)
clf4 = GradientBoostingClassifier(
    'deviance',
    learning_rate=0.1,
    n_estimators=256,
    subsample=0.8,
    random_state=None)
clf5 = GradientBoostingClassifier(
    'exponential',
    learning_rate=0.1,
    n_estimators=256,
    subsample=0.8,
    random_state=None)

classifiers = [clf1, clf2, clf3, clf4, clf5]
meta_classifier = LogisticRegression()
if __name__ == '__main__':
    from mlxtend.classifier import StackingCVClassifier
    from sklearn.model_selection import StratifiedKFold

    from sklearn.ensemble import StackingClassifier

    sclf = StackingCVClassifier(
        classifiers,
        meta_classifier,
        use_probas=True,
        cv=StratifiedKFold(5, True),
        use_features_in_secondary=False,
        stratify=True,
        shuffle=True,
        verbose=2,
        store_train_meta_features=False,
        use_clones=True)
