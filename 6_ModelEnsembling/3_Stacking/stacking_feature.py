def stacking_feature(clf, X, y, nb_cv=3, seed=42):
    """
    tfidf_lr = make_pipeline(TfidfVectorizer(), LogisticRegression())
    tfidf_lr.fit(X, y)
    tfidf_lr.predict_proba(X)
    """
    
    auc_loss = []
    pred_list = []
    
    kf = StratifiedKFold(nb_cv, True, seed).split(X, y)
    for i, (train_index, test_index) in enumerate(kf, 1):
        X_train, X_test, y_train, y_test = X[train_index], X[test_index], y[train_index], y[test_index]
        clf.fit(X_train, y_train)
        y_test_pred = clf.predict_proba(X_test)[:, 1] 
        pred_list += y_test_pred.tolist()
        auc_loss.append(roc_auc_score(y_test, y_test_pred))

    print("Auc-CV-Score: %0.5f (+/- %0.3f)" % (np.mean(auc_loss), np.std(auc_loss)))
    return pred_list
