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
df['n'] = 1

df = df.groupby('sex').agg({'n': 'count', 'label': 'sum'}).reset_index()

Y_true = 5.
N_true = 3.
y_i = df.label.values
n_i =(df.n-df.label).values

IV = np.sum((y_i/Y_true - n_i/N_true)*np.log(y_i/n_i/(Y_true/N_true)))
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