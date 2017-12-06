## stacking
```python
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB 
from sklearn.ensemble import RandomForestClassifier
from mlxtend.classifier import StackingClassifier
import numpy as np

clf1 = KNeighborsClassifier(n_neighbors=1)
clf2 = RandomForestClassifier(random_state=1)
clf3 = GaussianNB()
lr = LogisticRegression()
sclf = StackingClassifier(classifiers=[clf1, clf2, clf3], meta_classifier=lr, 
                          use_probas=True,
                          average_probas=False,
                          verbose=1,
                          use_features_in_secondary=True)

scores = model_selection.cross_val_score(sclf, X, y, cv=3, scoring='accuracy')
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()))
```

## stackingCV
```
from sklearn import model_selection
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB 
from sklearn.ensemble import RandomForestClassifier
from mlxtend.classifier import StackingCVClassifier
import numpy as np

RANDOM_SEED = 42
np.random.seed(RANDOM_SEED)

clf1 = KNeighborsClassifier(n_neighbors=1)
clf2 = RandomForestClassifier(random_state=RANDOM_SEED)
clf3 = GaussianNB()
clf4 = LGBMClassifier()
clf5 = XGBClassifier()

lr = LogisticRegression()

sclf = StackingCVClassifier(classifiers=[clf1, clf2, clf3, clf4, clf5], 
                            meta_classifier=lr,
                            use_probas=True, 
                            cv=3, 
                            use_features_in_secondary=True, 
                            stratify=True, 
                            shuffle=True, 
                            verbose=1)

scores = model_selection.cross_val_score(sclf, X, y, cv=3, scoring='accuracy') 
print("Accuracy: %0.2f (+/- %0.2f)" % (scores.mean(), scores.std()))
```
