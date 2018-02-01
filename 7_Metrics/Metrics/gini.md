```python

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
