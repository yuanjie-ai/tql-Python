> Gini = 2*AUC - 1
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
