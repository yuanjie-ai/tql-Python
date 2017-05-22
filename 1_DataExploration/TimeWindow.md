```
def slidingWindow(df,_id='id',time_col='time',label='label',observation_window=[],response_window=[]):
    observation = df.filter(col(time_col) >= observation_window[0]).filter(col(time_col) < observation_window[1]).drop(label)
    response = df.filter(col(time_col) >= response_window[0]).filter(col(time_col) < response_window[1]).select(_id,label)
    df = observation.join(response,_id).distinct()
    return(df)
```

- 表结构
> 用户标识、时间戳、标签
```test.cache()

DataFrame[stat_date: string, acct_no: string, is_buy_success: string, time: bigint]
```

```
res0 = spark.createDataFrame([(0,0,0,0)],['m','n','k','cr']).filter("m=-1")
for m in range(1,5):
    for n in range(1,6):
        for k in np.random.randint(300,size=10):
            observation_window = np.array([1451577600,1451577600+86400*m])
            response_window = np.array([observation_window[1],observation_window[1]+86400*n])
            res = slidingWindow(test,_id='acct_no',time_col='time',label='is_buy_success',
                                observation_window=observation_window+86400*k,
                                response_window=response_window+86400*k)
            res = res.groupBy('acct_no').agg(when(array_contains(collect_set('is_buy_success'),'Y'),1).otherwise(0).name('label'))
            res = res.agg(lit(m).name('m'),lit(n).name('n'),lit(k).name('k'),(F.sum('label')/count('label')).name('cr'))
            res0 = res0.union(res)
```
- result
> 观察时间窗口长度m 响应时间窗口长度n 同长度时间窗口下的不同时期k 转化率cr
```
re = res0.sort(desc('cr'),'m','n')
DataFrameWriter(re).saveAsTable("fbidm.time_window",mode='overwrite')
```