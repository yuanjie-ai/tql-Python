```
def getCorrelation(df, threshold=0.9, method='pearson'):
    corrMatrix = df.corr(method=method)
    ls = []
    _i = ''
    for i in df.columns:
        _ = corrMatrix[i][lambda x: abs(x) >= threshold][lambda x: x.index!=i].index.tolist()
        l = list(filter(lambda x: x != _i, _))
        if l:
            print('{:>22}'.format(i + ': '), l)
            ls.append(list(zip([i]*len(l), l)))
        _i = i
    return ls
```
