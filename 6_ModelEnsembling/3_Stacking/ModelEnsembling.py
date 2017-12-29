class ModelEnsembling(object):
    def __init__(self, classifiers, meta_classifier, cv=3, seed=42):
        self.classifiers = classifiers
        self.meta_classifier = meta_classifier
        self.skf = StratifiedKFold(n_splits=cv, shuffle=True, random_state=seed)

    def StackingCVClassifier(self, X, y, classifiers, meta_classifier, cv):
        sclf = StackingCVClassifier(classifiers=self.classifiers,
                                    meta_classifier=self.meta_classifier,
                                    use_probas=True,
                                    cv=cv,
                                    verbose=1)

        scores = cross_val_score(sclf, X, y, cv=self.skf.split(X, y), scoring='roc_auc', n_jobs=-1, verbose=1)
        print("Auc: %0.5f (+/- %0.5f)" % (scores.mean(), scores.std()))
        return scores
