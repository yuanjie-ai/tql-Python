<h1 align = "center">:rocket: 数据预处理 :facepunch:</h1>

---
## [不平衡数据][1]
---
# DataReshape

> 长变宽 各种工具等等

## 宽边长
```
def explode(df, col, pat=None, drop_col=True):
    """
    :param df:
    :param col: col name
    :param pat: String or regular expression to split on. If None, splits on whitespace
    :param drop_col: drop col is Yes or No
    :return: hive explode
    """
    data = df.copy()
    data_temp = data[col].str.split(pat=pat, expand=True).stack().reset_index(level=1, drop=True).rename(col+'_explode')
    if drop_col:
        data.drop(col, 1, inplace=True)
    return data.join(data_temp)
    
df = pd.DataFrame([[1, 'a b c'], 
                   [2, 'a b'],
                   [3, np.nan]], columns=['id', 'col'])

explode(df, 'col')
```
```
	id	col
0	1	a b c
1	2	a b
2	3	NaN


id	col_explode
0	1	a
0	1	b
0	1	c
1	2	a
1	2	b
2	3	NaN
```
- 一列变多列: df.a.str.split('|', expand=True)


---
[1]: https://www.jeremyjordan.me/imbalanced-data/
