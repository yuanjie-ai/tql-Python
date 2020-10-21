#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : Features
# @Time         : 2019-07-26 10:04
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : featuretools

import featuretools
import featuretools as ft
import featuretools.variable_types as vt

from tqdm.auto import tqdm
from tql.utils.pandas_utils import reduce_mem_usage, duplicate_columns
from tql.ml.automl.primitives import *
from featuretools.selection import remove_low_information_features, remove_single_value_features, \
    remove_highly_correlated_features


class AutoFeat(object):

    def __init__(self, id='ES'):
        self.es = ft.EntitySet(id=id)

    def add_entity(
            self, df, entity_id, type2features=None,
            index=None, time_index=None, secondary_time_index=None,
            normalize_entity=True,
    ):
        """

        :param df:
        :param entity_id: 表名
        :param type2features: vt.Categorical, vt.Boolean, vt.Id
        :param index:
        :param time_index:
        :param secondary_time_index:
        :return:
        """
        index = '__id' if index is None else index
        type2features = type2features if type2features is not None else {}

        variable_types = self._get_variable_types(self._convert_type(type2features))

        self.es.entity_from_dataframe(
            entity_id=entity_id,
            dataframe=df,
            index=index,
            variable_types=variable_types,
            time_index=time_index,
            secondary_time_index=secondary_time_index
        )

        if normalize_entity:
            self._normalize_entity(entity_id, variable_types)

    def add_relationship(self, parent_variable_name, child_variable_name):
        """
            relation = ft.Relationship(es['t1']['id'], es['t2']['id'])
            es.add_relationship(relation)
        :param parent_variable_name: (entity_id, id)
        :param child_variable_name: (entity_id, id)
        :return:
        """
        # relation = ft.Relationship(parent_variable, child_variable)
        relation = ft.Relationship(
            parent_variable=self.es[parent_variable_name[0]][parent_variable_name[1]],
            child_variable=self.es[child_variable_name[0]][child_variable_name[1]]
        )
        self.es.add_relationship(relation)

    def run_dfs(self,
                target_entity_id,
                max_depth=1,
                features_only=True,
                ignore_variables=None,
                reduce_mem=False,
                reduce_feats=True,
                trans_primitives=None,
                agg_primitives=None,
                chunk_size=None,
                n_jobs=1,
                **kwargs
                ):
        """Deep Feature Synthesisf
        agg_primitives (list[str or AggregationPrimitive], optional): List of Aggregation
            Feature types to apply.

                Default: ["sum", "std", "max", "skew", "min", "mean", "count", "percent_true", "num_unique", "mode"]
                DateTime: ['time_since_last', 'time_since_first', 'trend']

        trans_primitives (list[str or TransformPrimitive], optional):
            List of Transform Feature functions to apply.

                Default: ["day", "year", "month", "weekday", "haversine", "num_words", "num_characters"]

        groupby_trans_primitives (list[str or :class:`.primitives.TransformPrimitive`], optional):
            list of Transform primitives to make GroupByTransformFeatures with

        """
        if ignore_variables is None:
            # ignore_variables = [self.target_entity_id, self.index]
            # ignore_variables = ["__id"]  # 忽略单值id 会少了一些count特征
            ignore_variables = []

        if trans_primitives is None:
            trans_primitives = [
                "year", "month", "day", "hour", "minute", "week", "weekday", "is_weekend",
                'time_since_previous',
                # diff # https://stackoverflow.com/questions/60324672/how-is-time-since-previous-computed-in-featuretools
                Quarter(),
            ]

        _ = ft.dfs(
            entityset=self.es,
            target_entity=target_entity_id,  # 具有唯一ID: 不重复id的base_es或者normalize_entity生成的唯一id es
            features_only=features_only,
            max_depth=max_depth,
            # ignore_variables={self.entity_id: ignore_variables},
            chunk_size=chunk_size,
            n_jobs=n_jobs,
            verbose=1,
            agg_primitives=agg_primitives,
            trans_primitives=trans_primitives,
            **kwargs
        )

        if features_only:
            return _
        else:
            df = _[0]

            if reduce_feats:
                df = self._reduce_feats(df)

            if reduce_mem:
                df = reduce_mem_usage(df)

            df_bool = df.select_dtypes(bool)
            df.loc[:, df_bool.columns] = df_bool.astype(int)

            df_object = df.select_dtypes(object)
            df.loc[:, df_object.columns] = df_object.astype(float)

            return df.reset_index()

    def _reduce_feats(self, df):
        df = remove_low_information_features(df)
        df = remove_single_value_features(df, count_nan_as_value=True)
        df.drop(duplicate_columns(df), 1, inplace=True)
        return df

    def _normalize_entity(self, entity_id, variable_types):
        normalize_entity_feats = []
        for feat, type_ in variable_types.items():
            if type_ in {vt.Id, vt.Categorical, vt.Boolean} and feat != self.es[entity_id].index:
                normalize_entity_feats.append(feat)

        with tqdm(normalize_entity_feats) as t:
            for feat in t:
                t.set_description(f"NormalizeEntity[{feat}]")
                self.es.normalize_entity(entity_id, feat, feat)

    def _get_variable_types(self, type2features):
        dic = {}
        for type_, features in type2features.items():
            dic.update(zip(features, len(features) * [type_]))
        return dic

    def _convert_type(self, type2features):
        type2features_ = {}
        for type_, features in type2features.items():
            if isinstance(type_, str):
                type2features_[vt.__getattribute__(type_)] = features
            else:
                type2features_[type_] = features

        return type2features_


if __name__ == '__main__':
    import pandas as pd

    df = pd.DataFrame([[1, 2, 3], [2, 2, 3], [3, 2, 3]], columns=['uid', 'a', 'b'])
    df['date'] = pd.date_range('2020-01-01', periods=3)

    type2features = {
        'Id': ['uid'],
        'Categorical': ['a', 'b'],
        'Datetime': ['date']
    }

    af = AutoFeat()
    af.add_entity(df, 'demo', type2features, index='uid')
    # af.add_relationship((), ())

    df_ft = af.run_dfs('demo', 3, False, reduce_feats=False)

    print(df_ft)
