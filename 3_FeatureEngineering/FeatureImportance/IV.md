## IV
- python
```
a = [['A', 1],
     ['A', 1],
     ['A', 1],
     ['A', 0],
     ['B', 1],
     ['B', 1],
     ['B', 0],
     ['B', 0]]
df = pd.DataFrame(a, columns=['sex', 'label'])

def iv(df):
    """
    仅支持离散型特征
    """
    Y_true = (df.label==1).sum()
    N_true = (df.label==0).sum()
    strColName = df.columns.tolist()
    strColName.remove('label')
    iv = []
    for i in strColName:
        data = df.groupby(i)['label'].agg(['count', 'sum']).reset_index()
        y_i = data['sum'].values
        n_i =(data['count']-data['sum']).values
        iv.append(np.sum((y_i/Y_true - n_i/N_true)*np.log((y_i+0.000001)/(n_i+0.000001)/(Y_true/N_true))))
    return sorted(zip(iv, strColName), reverse=True)
```
