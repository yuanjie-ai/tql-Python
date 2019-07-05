> 单调分档是一种广泛用于记分卡开发的数据准备技术，通常用SAS实现。 下面是尝试用python进行单调分类
---
```python
import numpy as np
import pandas as pd
import scipy.stats.stats as stats
from sklearn.datasets import load_iris
iris = load_iris()
X, y = iris.data, iris.target

# define a binning function
def mono_bin(Y, X, n = 20):
  # fill missings with median
  X2 = X.fillna(np.median(X))
  r = 0
  while np.abs(r) < 1:
    d1 = pd.DataFrame({"X": X2, "Y": Y, "Bucket": pd.qcut(X2, n, duplicates='drop')})
    d2 = d1.groupby('Bucket', as_index = True)
    r, p = stats.spearmanr(d2.mean().X, d2.mean().Y)
    n = n - 1
  d3 = pd.DataFrame(d2.min().X, columns = ['min_' + X.name])
  d3['max_' + X.name] = d2.max().X
  d3[Y.name] = d2.sum().Y
  d3['total'] = d2.count().Y
  d3[Y.name + '_rate'] = d2.mean().Y
  d4 = (d3.sort_index(by = 'min_' + X.name)).reset_index(drop = True)
  print("=" * 60)
  print(d4)
  
mono_bin(data.label, data.a)
mono_bin(data.label, data.b)
mono_bin(data.label, data.c)
mono_bin(data.label, data.d)
```

```
============================================================
  min_a  max_a  label  total  label_rate
0   NaN    4.9    1.0     21    0.047619
1   NaN    5.1    3.0     19    0.157895
2   NaN    5.4    2.0     11    0.181818
3   NaN    5.7   15.0     19    0.789474
4   NaN    6.1   13.0     14    0.928571
5   NaN    7.0   16.0     16    1.000000
============================================================
  min_b  max_b  label  total  label_rate
0   NaN    2.8   27.0     28    0.964286
1   NaN    3.0   15.0     22    0.681818
2   NaN    3.4    8.0     29    0.275862
3   NaN    4.4    0.0     21    0.000000
============================================================
  min_c  max_c  label  total  label_rate
0   NaN    1.5    0.0     37     0.00000
1   NaN    4.1   19.0     32     0.59375
2   NaN    5.1   31.0     31     1.00000
============================================================
  min_d  max_d  label  total  label_rate
0   NaN    0.2    0.0     34    0.000000
1   NaN    1.3   28.0     44    0.636364
2   NaN    1.8   22.0     22    1.000000
```
