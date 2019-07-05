- https://www.kaggle.com/c/home-credit-default-risk/discussion/64821
- Could you please give more detailed explanation about your approach to feature selection with Ridge Regression?

- 1. Train a ridge on a subset of features.
- 2. Calculate AUC.
- 3. Add features, one at a time. Train ridge. If AUC improves, keep the feature. If not, discard the feature.

> Yup. Turns out, for AUC it doesn't matter if you are using it as continuous or discrete. You can use Logistic Regression instead, but I usually find that Ridge has better score and is easier to work with.




> pip install sklearn-genetic

https://www.tensorflow.org/guide/keras

https://www.tensorflow.org/guide/feature_columns#categorical_identity_column

https://www.kaggle.com/c/home-credit-default-risk/discussion/64510