> Gini = 2*AUC - 1: `2*roc_auc_score(a, p)-1`
```python
def ginic(actual, pred):
    actual = np.asarray(actual)  # In case, someone passes Series or list
    n = len(actual)
    a_s = actual[np.argsort(pred)]
    a_c = a_s.cumsum()
    giniSum = a_c.sum() / a_s.sum() - (n + 1) / 2.0
    return giniSum / n

def gini_normalizedc(a, p):
    if p.ndim == 2:  # Required for sklearn wrapper
        p = p[:, 1]  # If proba array contains proba for both 0 and 1 classes, just pick class 1
    return ginic(a, p) / ginic(a, a)
```

```
from numba import jit

@jit
def eval_gini(y_true, y_prob):
    y_true = np.asarray(y_true)
    y_true = y_true[np.argsort(y_prob)]
    ntrue = 0
    gini = 0
    delta = 0
    n = len(y_true)
    for i in range(n-1, -1, -1):
        y_i = y_true[i]
        ntrue += y_i
        gini += y_i * delta
        delta += 1 - y_i
    gini = 1 - 2 * gini / (ntrue * (n - ntrue))
    return gini
```


- Tensorflow
```python
def gini_normalized(actual, pred):
    n = tf.shape(actual)[1]
    indices = tf.nn.top_k(pred, k=n)[1][0]
    actual_sorted = tf.gather(actual[0], indices)
    cost = tf.reduce_sum(actual_sorted)
    loss_proportion = tf.cumsum(actual_sorted) / cost
    null_model = tf.to_float(tf.range(1, n + 1)) / tf.to_float(n)
    g = tf.subtract(loss_proportion, null_model)
    g = tf.reduce_sum(g) / tf.to_float(n)
    g /= (1.0 - tf.reduce_mean(actual)) / 2.0
    return g
```
