```python
es.entity_from_dataframe(
    entity_id,  # 表名
    dataframe,  # 表
    variable_types={'example': ft.variable_types.Categorical},  # 字段类型
    make_index=False, index=None,  # 数据框中没有（主键）唯一的索引，生成索引并指定一个索引名
    time_index=None,  # 第一时间索引
    secondary_time_index=None,  # 第二时间索引
    encoding=None,
    already_sorted=False # 默认数据框未按时间排序
)

ft.dfs(
    entityset=None,
    target_entity=None,
    agg_primitives=None,
    trans_primitives=None,
    max_depth=None,
    max_features=None,
    n_jobs=1,
    verbose=False,
    save_progress='./',
    chunk_size=None,
    
    features_only=False,
    drop_contains=None, drop_exact=None,  # 删除带有固定字符串或者匹配到的字符串特征
    instance_ids=None,
    ignore_entities=None,
    ignore_variables=None,

    cutoff_time=None,
    cutoff_time_in_index=False,
    training_window=None,
    approximate=None,

    where_primitives=None
)
```
