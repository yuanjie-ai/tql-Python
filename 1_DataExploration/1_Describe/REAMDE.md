<h1 align = "center">:rocket: 描述性统计 :facepunch:</h1>

---

```python
import DataFrameSummary # from pandas_summary import DataFrameSummary
dfs = DataFrameSummary(df)
```

- 列类型: dfs.columns_types
```python
numeric     9
bool        3
categorical 2
unique      1
date        1
constant    1
dtype: int64
```

- 列统计: dfs.columns_stats

```python
                      A            B        C          D          E 
counts             5802         5794     5781       5781       4617   
uniques            5802            3     5771        128        121   
missing               0            8       21         21       1185   
missing_perc         0%        0.14%    0.36%      0.36%     20.42%   
types            unique  categorical  numeric    numeric    numeric 
```

- 相关系数矩阵: dfs.corr

|cor|a|b|c|d|
|:--:|:--:|:--:|:--:|:--:|
|a	|1.000000	|-0.109369  |0.871754	|0.817954|
|b	|-0.109369  |1.000000   |-0.420516  |-0.356544|
|c	|0.871754	|-0.420516  |1.000000	|0.962757|
|d	|0.817954	|-0.356544  |0.962757	|1.000000|


- 列汇总: 单列dfs['a'], 所有列dfs.summary()
```python
std                                                                 0.2827146
max                                                                  1.072792
min                                                                         0
variance                                                           0.07992753
mean                                                                0.5548516
5%                                                                  0.1603367
25%                                                                 0.3199776
50%                                                                 0.4968588
75%                                                                 0.8274732
95%                                                                  1.011255
iqr                                                                 0.5074956
kurtosis                                                            -1.208469
skewness                                                            0.2679559
sum                                                                  3207.597
mad                                                                 0.2459508
cv                                                                  0.5095319
zeros_num                                                                  11
zeros_perc                                                               0,1%
deviating_of_mean                                                          21
deviating_of_mean_perc                                                  0.36%
deviating_of_median                                                        21
deviating_of_median_perc                                                0.36%
top_correlations                                         c: 87.18%, d: 81.80%
counts                                                                   5781
uniques                                                                  5771
missing                                                                    21
missing_perc                                                            0.36%
types                                                                 numeric
Name: A, dtype: object
```
