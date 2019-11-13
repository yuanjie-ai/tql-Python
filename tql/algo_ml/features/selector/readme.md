- https://www.kaggle.com/c/home-credit-default-risk/discussion/64821
- Could you please give more detailed explanation about your approach to feature selection with Ridge Regression?

- 1. Train a ridge on a subset of features.
- 2. Calculate AUC.
- 3. Add features, one at a time. Train ridge. If AUC improves, keep the feature. If not, discard the feature.

> Yup. Turns out, for AUC it doesn't matter if you are using it as continuous or discrete. You can use Logistic Regression instead, but I usually find that Ridge has better score and is easier to work with.

4.1 Chris的单特征筛选方案
    该方案的核心思想很简单,如果我的一个特征在训练集上训练完之后在验证集上的预测结果的auc低于0.5，那么这个特征很大概率是一个噪音特征。这个我用lgb作为基础模型进行了尝试，发现不仅特征筛选快，而且确实效果不错。大家也可以作为自己机器学习技能库中的一块收藏。

4.2 Permutation importance特征筛选方案
    Permutation importance特征筛选的方案大致思路就是，我训练好了一个模型，我们对验证集中的某一个特征列进行shuffle，如果对shuffle之后的特征进行预测的准确性没有变化甚至变好了，那么这个特征可能意义不大，可以毫不犹豫的进行删除,如果预测结果变差了，那么该特征是非常重要的，不可以删除。


> pip install sklearn-genetic

https://www.tensorflow.org/guide/keras

https://www.tensorflow.org/guide/feature_columns#categorical_identity_column

https://www.kaggle.com/c/home-credit-default-risk/discussion/64510