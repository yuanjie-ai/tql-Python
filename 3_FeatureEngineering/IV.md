# IV
- python
```
a = np.array([['A', 1.],
              ['A', 1.],
              ['A', 1.],
              ['A', 0.],
              ['B', 1.],
              ['B', 1.],
              ['B', 0.],
              ['B', 0.]])
df = pd.DataFrame(a, columns=['sex', 'label'])

def iv(df):
    """
    仅支持离散型特征
    """
    Y_true = (df.label==1).sum()
    N_true = (df.label==0).sum()
    features = df.columns.tolist()
    features.remove('label')
    iv = []
    for i in features:
        data = df.groupby(i)['label'].agg(['count', 'sum']).reset_index()
        y_i = data['sum'].values
        n_i =(data['count']-data['sum']).values
        iv.append(np.sum((y_i/Y_true - n_i/N_true)*np.log(y_i/n_i/(Y_true/N_true))))
    return sorted(zip(iv, features), reverse=True)
```
- pyspark
```
spark_df = spark.createDataFrame(a.tolist(), ['sex', 'label'])
spark_df = spark_df.groupBy('sex').agg({'sex': 'count', 'label': 'sum'}).toDF('sex', 'n', 'label')
spark_df.show()
+---+---+-----+
|sex|  n|label|
+---+---+-----+
|  B|  4|  2.0|
|  A|  4|  3.0|
+---+---+-----+

Y_true = 5.
N_true = 3.
y_i = col('label')
n_i = col('n') - col('label')

IV = sum((y_i/Y_true - n_i/N_true)*log(y_i/n_i/(Y_true/N_true)))

spark_df.agg(IV.name('iv')).show()
+------------------+
|                iv|
+------------------+
|0.2929632769781626|
+------------------+
```
