## IV
> 常用在评分卡
- 小于0.02预测能力无
- 大于0.30预测能力强
```python
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
    Y_true = (df.label==1).sum()
    N_true = (df.label==0).sum()
    colName = df.columns.tolist()
    colName.remove('label')
    iv = []
    for i in colName:
        data = df.groupby(i)['label'].agg(['count', 'sum']).reset_index()
        y_i = data['sum'].values
        n_i =(data['count']-data['sum']).values
        iv.append(np.sum((y_i/Y_true - n_i/N_true)*np.log((y_i+0.000001)/(n_i+0.000001)/(Y_true/N_true))))
    return sorted(zip(iv, colName), reverse=True)
```
