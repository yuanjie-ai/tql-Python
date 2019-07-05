# :rocket: [Windowing and Analytics Functions][1] :facepunch:
```
COUNT(DISTINCT a) OVER (PARTITION BY c)
```
---
```
df1 = spark.range(5).withColumn('a', lit(8))
df2 = spark.range(5, 10).withColumn('a', lit(88))
df = df1.union(df2)

+---+---+
| id|  a|
+---+---+
|  0|  8|
|  1|  8|
|  2|  8|
|  3|  8|
|  4|  8|
|  5| 88|
|  6| 88|
|  7| 88|
|  8| 88|
|  9| 88|
+---+---+
```
---
## RankingFunctions
- ROW_NUMBER
```
row_number() OVER(PARTITION BY xx ORDER BY xx)
row_number().over(Window.partitionBy("xx").orderBy("xx"))
```
- RANK: 排名相等留下空位(1,2,2,4,5)
- DENSE_RANK: 排名相等不留空位(1,2,2,3,4)
- PERCENT_RANK: 分位数分布
- NTILE: ntile(n): 1/n比例切割
```
df.withColumn('new',expr("ntile(5) OVER(PARTITION BY a ORDER BY id) ")).show()

+---+---+---+
| id|  a|new|
+---+---+---+
|  5| 88|  1|
|  6| 88|  2|
|  7| 88|  3|
|  8| 88|  4|
|  9| 88|  5|
|  0|  8|  1|
|  1|  8|  2|
|  2|  8|  3|
|  3|  8|  4|
|  4|  8|  5|
+---+---+---+
```
---
## Analytic functions
- first(col, ignorenulls=False): first(xx) OVER(PARTITION BY xx ORDER BY xx DESC)
- last(col, ignorenulls=False): last(xx) OVER(PARTITION BY xx ORDER BY xx DESC)
- CUME_DIST: 累积分布
```
df.withColumn('new',expr("cume_dist() OVER(PARTITION BY a ORDER BY id) ")).show()

+---+---+---+
| id|  a|new|
+---+---+---+
|  5| 88|0.2|
|  6| 88|0.4|
|  7| 88|0.6|
|  8| 88|0.8|
|  9| 88|1.0|
|  0|  8|0.2|
|  1|  8|0.4|
|  2|  8|0.6|
|  3|  8|0.8|
|  4|  8|1.0|
+---+---+---+
```
- lead(col, count=1, default=None): 向上滑动
```
df.withColumn('new',expr("lead(id) OVER(PARTITION BY a order by id) ")).show()
+---+---+----+
| id|  a| new|
+---+---+----+
|  5| 88|   6|
|  6| 88|   7|
|  7| 88|   8|
|  8| 88|   9|
|  9| 88|null|
|  0|  8|   1|
|  1|  8|   2|
|  2|  8|   3|
|  3|  8|   4|
|  4|  8|null|
+---+---+----+
```
- lag(col, count=1, default=None): 向下滑动
```
df.withColumn('new',expr("lag(id) OVER(PARTITION BY a order by id) ")).show()
+---+---+----+
| id|  a| new|
+---+---+----+
|  5| 88|null|
|  6| 88|   5|
|  7| 88|   6|
|  8| 88|   7|
|  9| 88|   8|
|  0|  8|null|
|  1|  8|   0|
|  2|  8|   1|
|  3|  8|   2|
|  4|  8|   3|
+---+---+----+
```
- 聚合函数: max/min/mean/sum...(可滑动/广播)
```
df.withColumn('new',expr("id - mean(id) OVER() ")).show()
+---+---+----+
| id|  a| new|
+---+---+----+
|  0|  8|-4.5|
|  1|  8|-3.5|
|  2|  8|-2.5|
|  3|  8|-1.5|
|  4|  8|-0.5|
|  5| 88| 0.5|
|  6| 88| 1.5|
|  7| 88| 2.5|
|  8| 88| 3.5|
|  9| 88| 4.5|
+---+---+----+

df.withColumn('new',expr("mean(id) OVER(PARTITION BY a) ")).show()
+---+---+---+
| id|  a|new|
+---+---+---+
|  5| 88|7.0|
|  6| 88|7.0|
|  7| 88|7.0|
|  8| 88|7.0|
|  9| 88|7.0|
|  0|  8|2.0|
|  1|  8|2.0|
|  2|  8|2.0|
|  3|  8|2.0|
|  4|  8|2.0|
+---+---+---+
```
[1]: https://cwiki.apache.org/confluence/display/Hive/LanguageManual+WindowingAndAnalytics
