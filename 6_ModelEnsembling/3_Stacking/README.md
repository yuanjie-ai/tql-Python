## 通用
```python
import numpy as np
from sklearn.datasets import load_iris
from sklearn.model_selection import cross_val_score
from sklearn.linear_model import LogisticRegression
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC # not proba
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors import RadiusNeighborsClassifier # not proba
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import GradientBoostingClassifier
from xgboost.sklearn import XGBClassifier
from lightgbm.sklearn import LGBMClassifier

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

iris = load_iris()
X = iris.data
y = iris.target

# clf11 = RadiusNeighborsClassifier() # not proba
# clf12 = SVC() # not proba
clf1 = LogisticRegression()
clf2 = RandomForestClassifier()
clf3 = GradientBoostingClassifier()
clf4 = GaussianNB()
clf5 = KNeighborsClassifier()
clf6 = MLPClassifier()
clf7 = LGBMClassifier()
clf8 = XGBClassifier()

clfs = [clf1, clf2, clf3, clf4, clf5, clf6, clf7, clf8]
lr = LogisticRegression()
```

## StackingClassifier
```python
sclf = StackingClassifier(classifiers=clfs, 
                          meta_classifier=lr, 
                          use_probas=True,
                          average_probas=False,
                          verbose=1)

scores = cross_val_score(sclf, X, y, cv=3, scoring='accuracy')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()))
```

## StackingCVClassifier
```python


sclf = StackingCVClassifier(classifiers=clfs, 
                            meta_classifier=lr,
                            use_probas=True, 
                            cv=3, 
                            verbose=1)

skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42) # .split(X, y)
scores = cross_val_score(sclf, X, y, cv=skf, scoring='accuracy') 
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()))
```

## EnsembleVoteClassifier
```python
eclf = EnsembleVoteClassifier(clfs=clfs, voting='hard', weights=[1]*len(clfs))
scores = cross_val_score(eclf, X, y, cv=3, scoring='accuracy')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()))
```
