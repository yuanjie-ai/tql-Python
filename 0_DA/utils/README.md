```python
# ips_as_sentence  
def feat(df=df.head(100), feat_name = ('app', 'ip')):
        return df.groupby(feat_name[0])[feat_name[1]].agg(lambda x: ' '.join(map(str, x))).values
```
