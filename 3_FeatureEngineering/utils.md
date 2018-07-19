- 统计特征
```python
def get_desc_feats(data, gr='PERSONID', feats=[f"FTR{i}" for i in range(51)]):
    for _FTR in tqdm_notebook(feats):
        _columns = {i: _FTR + '_' + i for i in ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']}
        gr = data.groupby(gr)[_FTR]
        def f():
            df = gr.describe().reset_index().rename(columns=_columns)
            df[_FTR + '_' + 'kurt'] = gr.apply(pd.DataFrame.kurt).values
            df[_FTR + '_' + 'skew'] = gr.skew().values
            df[_FTR + '_' + 'sem'] = gr.sem().values
            df[_FTR + '_' + 'sum'] = gr.sum().values
            return df

        if _FTR=='FTR0':
            df = f()
        else:
            df = df.merge(f(), 'left', gr)
    return df
```
