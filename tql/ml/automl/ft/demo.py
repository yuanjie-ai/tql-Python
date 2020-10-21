#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : OneTable
# @Time         : 2020/9/4 11:13 上午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://www.cnblogs.com/dogecheng/p/12659605.html
# https://www.jianshu.com/p/71782dbe2e1e
# https://github.com/scottlinlin/auto_feature_demo
# cutoff_time + training_window
# https://www.kaggle.com/frednavruzov/auto-feature-generation-featuretools-example/comments#736827
# https://www.kaggle.com/willkoehrsen/tuning-automated-feature-engineering-exploratory/comments#880162

import featuretools as ft

from sklearn.datasets import load_iris
import pandas as pd
import numpy as np
from tql.algo_ml.cv import LGBMClassifierCV
from sklearn.metrics import accuracy_score
from lightgbm import LGBMClassifier

primitives = ft.list_primitives().groupby('type')['name'].agg(list)
trans_primitives, agg_primitives = primitives['transform'], primitives['aggregation']

dataset = load_iris()
X = dataset.data[:100]
y = dataset.target[:100]
iris_feature_names = dataset.feature_names

df = pd.DataFrame(X, columns=iris_feature_names)
df.head()

# 单表
es = ft.EntitySet(id='one_df')
entity_id = 'entity_id'
es.entity_from_dataframe(
    entity_id=entity_id,
    dataframe=df.copy(),
    index='index',  # If None, take the first column
    make_index=True,
    # variable_types={'Sex': ft.variable_types.Boolean}
)

# relation = ft.Relationship(es['df_1']['id'], es['df_2']['id'])
# es = es.add_relationship(relation)
# 若要对类别变量做聚合表征需要拆分实体
es.normalize_entity # 可以考虑把强特分离出来做交叉特征【专注】Creating a normalized entity to cross throught our main interest table¶
# es = es.normalize_entity(base_entity_id='entity_id', new_entity_id='new_entity_id', index='Pclass')
# es = es.normalize_entity(base_entity_id='entity_id', new_entity_id='Sex', index='Sex')
trans_primitives = ['add_numeric', 'subtract_numeric', 'multiply_numeric', 'divide_numeric']  # 2列相加减乘除来生成新特征
# ft.list_primitives()  # 查看可使用的特征集元
feature_matrix, feature_names = ft.dfs(entityset=es,
                                       target_entity='iris', # 具有唯一id
                                       max_depth=2,  # max_depth=1，只在原特征上进行运算产生新特征
                                       verbose=1,
                                       trans_primitives=trans_primitives, # 顺序影响结果,
                                       features_only=True # debug 生成的特征
                                       )

# 针对分组统计，NUM_UNIQUE, MODE

class Featurer(object):

    def __init__(self, es: ft.EntitySet, trans_primitives):
        self.es = es


def post_process(feature_matrix, run_mode='TRAIN', missing_threshold=0.95, correlation_threshold=0.95):
    print('Run mode : {}.'.format(run_mode))
    if (run_mode == 'TRAIN'):
        print('Feature matrix post processing missing_threshold : {} , correlation_threshold : {}'.format(
            missing_threshold, correlation_threshold))
    print('Dimensionality before post processing : {}.'.format(feature_matrix.shape))

    #### Remove duplicated features
    start_features = feature_matrix.shape[1]
    feature_matrix = feature_matrix.iloc[:, ~feature_matrix.columns.duplicated()]
    n_duplicated = start_features - feature_matrix.shape[1]
    print(f'Number of duplicated features : {n_duplicated}')

    #### Replace infinity values with missing values
    feature_matrix = feature_matrix.replace({np.inf: np.nan, -np.inf: np.nan}).reset_index()

    #### Treat features with missing values
    # Missing values statistics
    missing = pd.DataFrame(feature_matrix.isnull().sum())
    missing['fraction'] = missing[0] / feature_matrix.shape[0]
    missing.sort_values('fraction', ascending=False, inplace=True)
    # Missing above threshold
    missing_cols = list(missing[missing['fraction'] > missing_threshold].index)
    n_missing_cols = len(missing_cols)
    # Remove missing columns
    feature_matrix = feature_matrix[[x for x in feature_matrix if x not in missing_cols]]
    print('Number of features with missing values above {} : {}'.format(missing_threshold, n_missing_cols))

    # Fill missing values with 0
    feature_matrix.fillna(0, inplace=True)

    if (run_mode == 'TEST'):
        return feature_matrix

    #### Treat Zero variance features
    # Variance statistics
    unique_counts = pd.DataFrame(feature_matrix.nunique()).sort_values(0, ascending=True)
    zero_variance_cols = list(unique_counts[unique_counts[0] == 1].index)
    n_zero_variance_cols = len(zero_variance_cols)
    # Remove zero variance features
    feature_matrix = feature_matrix[[x for x in feature_matrix if x not in zero_variance_cols]]
    print('Number of zero variance features : {}'.format(n_zero_variance_cols))

    #### Treat highly correlated features
    # Calculate Correlations
    corr_matrix = feature_matrix.corr()
    # Extract the upper triangle of the correlation matrix
    upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(np.bool))
    # print(upper)

    # Select the features with abolute correlation value above the threshold
    to_drop = [column for column in upper.columns if any(upper[column].abs() > correlation_threshold)]
    # print(to_drop)
    n_collinear = len(to_drop)
    feature_matrix = feature_matrix[[x for x in feature_matrix if x not in to_drop]]
    print(
        'Highly correlated columns removed with correlation above {} : {} '.format(correlation_threshold, n_collinear))

    total_removed = n_duplicated, n_missing_cols + n_zero_variance_cols + n_collinear

    print('Total columns removed: ', total_removed)
    print('Dimensionality after post processing: {}'.format(feature_matrix.shape))

    feature_names = feature_matrix.columns

    return feature_matrix, feature_names
