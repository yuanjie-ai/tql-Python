## 1. msno.matrix: 行列缺失值个数
```python
import missingno as msno
np.random.seed(888)
null_pattern = (np.random.random(1000).reshape((50, 20)) > 0.5).astype(bool)
null_pattern = pd.DataFrame(null_pattern).replace({False: None})

msno.matrix(null_pattern.set_index(pd.period_range('1/1/2011', '2/1/2015', freq='M')), color=(1, 0, 0))
```

## 2. msno.bar: 列缺失值个数
```python
msno.bar(null_pattern, color=(1, 0, 0), log=True)
```

## 3. Heatmap: 缺失特征相关性
```python
msno.heatmap(null_pattern)
```

## 4. msno.nullity_filter: 缺失值列筛选
```python
# 缺失率大于0.9
msno.nullity_filter(_data, filter='bottom', p=1-0.9)

# 缺失率小于0.9
msno.nullity_filter(_data, filter='top', p=1-0.9)
```
