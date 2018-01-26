

## 有监督编码
- TargetEncoder
- LeaveOneOutEncoder
```python
s = cross_val_score(make_pipeline(TargetEncoder(), lr), X.values, y, cv=skf, n_jobs=3)
s = cross_val_score(make_pipeline(LeaveOneOutEncoder(), lr), X.values, y, cv=skf, n_jobs=3)
s
s.mean()
s.std()
```

## 非监督编码
```python
import pandas as pd
import category_encoders
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import StratifiedKFold, cross_val_score

skf = StratifiedKFold(n_splits=3, shuffle=True, random_state=42)
clf = LogisticRegression()
encoder_names = category_encoders.__all__
ls = []
for encoder_name in encoder_names:
    encoder = getattr(category_encoders, encoder_name)
    _X = encoder().fit_transform(X, y)
    scores = cross_val_score(clf, _X, y, cv=skf, n_jobs=3)
    ls.append([scores.mean(), scores.std(), encoder_name])
df_score = pd.DataFrame(ls, columns=['scores_mean', 'scores_std', 'encoder']) \
    .sort_values(['scores_mean', 'scores_std'], ascending=False)

```
