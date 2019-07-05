```python
def getCorrelationFeatures(df, threshold=0.9, method='pearson'):
    corrMatrix = df.corr(method=method)
    _dic = {}
    for col in df.columns:
        l = corrMatrix[col][col:][1:][lambda x: abs(x) >= threshold].index.tolist()
        if l:
            print('{:<22}'.format(col + ': '), l)
            _dic[col] = l
    return _dic
```
