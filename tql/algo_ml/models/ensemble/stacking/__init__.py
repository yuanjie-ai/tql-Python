# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# """
# __title__ = '__init__.py'
# __author__ = 'JieYuan'
# __mtime__ = '19-1-11'
# """
#
# ## 将xgb和lgb结果进行stacking
# train_stack = np.vstack([oof_lgb, oof_xgb]).transpose()
# test_stack = np.vstack([predictions_lgb, predictions_xgb]).transpose()
#
# folds_stack = RepeatedKFold(n_splits=5, n_repeats=2, random_state=2019)
# oof_stack = np.zeros(train_stack.shape[0])
# predictions = np.zeros(test_stack.shape[0])
#
# for fold_, (trn_idx, val_idx) in enumerate(folds_stack.split(train_stack, target)):
#     print("fold {}".format(fold_))
#     trn_data, trn_y = train_stack[trn_idx], target.iloc[trn_idx].values
#     val_data, val_y = train_stack[val_idx], target.iloc[val_idx].values
#
#     clf_3 = BayesianRidge()
#     clf_3.fit(trn_data, trn_y)
#
#     oof_stack[val_idx] = clf_3.predict(val_data)
#     predictions += clf_3.predict(test_stack) / 10
#
# print("CV score: {:<8.8f}".format(mean_absolute_error(oof_stack, target)))
# print('final score: {:<8.8f}'.format(1 / (1 + mean_absolute_error(oof_stack, target))))