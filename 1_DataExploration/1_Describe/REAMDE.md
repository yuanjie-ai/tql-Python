:rocket: 描述性统计 :facepunch:
---
```python
import DataFrameSummary # from pandas_summary import DataFrameSummary
dfs = DataFrameSummary(df)
```

- getting the columns types
```python
dfs.columns_types


numeric     9
bool        3
categorical 2
unique      1
date        1
constant    1
dtype: int64
```

- getting the columns stats

```python
dfs.columns_stats


                      A            B        C              D              E 
counts             5802         5794     5781           5781           4617   
uniques            5802            3     5771            128            121   
missing               0            8       21             21           1185   
missing_perc         0%        0.14%    0.36%          0.36%         20.42%   
types            unique  categorical  numeric        numeric        numeric 
```

- getting a single column summary, e.g. numerical column
```python
# we can also access the column using numbers A[1]
dfs['A']

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
top_correlations                         {u'D': 0.702240243124, u'E': -0.663}
counts                                                                   5781
uniques                                                                  5771
missing                                                                    21
missing_perc                                                            0.36%
types                                                                 numeric
Name: A, dtype: object
```
