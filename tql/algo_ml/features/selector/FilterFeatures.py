#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'FilterFeatures'
__author__ = 'JieYuan'
__mtime__ = '19-1-24'
"""
from ....utils.time import timer

import pandas as pd
from functools import partial
from tqdm import tqdm
from concurrent.futures import ProcessPoolExecutor

"""https://www.cnblogs.com/nolonely/p/6435083.html
1、为什么要做特征选择
在有限的样本数目下，用大量的特征来设计分类器计算开销太大而且分类性能差。
2、特征选择的确切含义
将高维空间的样本通过映射或者是变换的方式转换到低维空间，达到降维的目的，然后通过特征选取删选掉冗余和不相关的特征来进一步降维。
3、特征选取的原则
获取尽可能小的特征子集，不显著降低分类精度、不影响类分布以及特征子集应具有稳定适应性强等特点
"""


class FilterFeatures(object):
    """粗筛
    高缺失率：
    低方差（高度重复值）：0.5%~99.5%分位数内方差为0的初筛
    高相关：特别高的初筛，根据重要性细筛
    低重要性：
    召回高IV：
    """

    def __init__(self, df: pd.DataFrame, exclude=None):
        self.to_drop_dict = {}
        if exclude is None:
            exclude = []

        assert isinstance(exclude, list)
        assert isinstance(df, pd.DataFrame)

        self.df = df

        exclude += df.select_dtypes(['datetime64[ns]', object]).columns.tolist()
        print(f"Exclude Fetures: {exclude}")

        if exclude:
            self.feats = df.columns.difference(exclude).tolist()
        else:
            self.feats = df.columns.tolist()

    def run(self):
        df = self.df.copy()

        with timer('干掉高缺失'):
            self.to_drop_dict['filter_missing'] = self.filter_missing()


        with timer('干掉低方差'):
            self.to_drop_dict['filter_variance'] = self.filter_variance()


        with timer('干掉高相关'):
            pass

        return df

    def filter_missing(self, feats=None, threshold=0.95):
        """
        :param feat_cols:
        :param threshold:
        :param as_na: 比如把-99当成缺失值
        :return:
        """
        if feats is None:
            feats = self.feats

        to_drop = self.df[feats].isna().mean()[lambda x: x > threshold].index.tolist()
        print('%d features with greater than %0.2f missing values.' % (len(to_drop), threshold))
        return to_drop

    def _filter_variance(self, feat, df):
        var = df[feat][lambda x: x.between(x.quantile(0.005), x.quantile(0.995))].var()
        return '' if var else feat

    def filter_variance(self, feats=None, max_worker=4):
        if feats is None:
            feats = self.feats

        _filter_variance = partial(self._filter_variance, df=self.df)
        with ProcessPoolExecutor(min(max_worker, len(feats))) as pool:
            to_drop = pool.map(_filter_variance, tqdm(feats, 'Filter Variance ...'))
            to_drop = [feat for feat in to_drop if feat]
        print('%d features with 0 variance in 0.5 ~ 99.5 quantile.' % len(to_drop))
        return to_drop

    # def filter_correlation(self, feat_cols=None, threshold=0.98):
    #     if feat_cols is None:
    #         feat_cols = self.feats
    #
    #     print('Compute Corr Matrix ...')
    #     corr_matrix = self.df[feat_cols].corr().abs()
    #
    #     # Extract the upper triangle of the correlation matrix
    #     upper = pd.DataFrame(np.triu(corr_matrix, 1), feat_cols, feat_cols)
    #
    #     # Select the features with correlations above the threshold
    #     # Need to use the absolute value
    #     to_drop = [column for column in tqdm(upper.columns, 'Correlation Filter') if any(upper[column] > threshold)]
    #
    #     self.to_drop_correlation = to_drop
    #
    #     # Dataframe to hold correlated pairs
    #     # Iterate through the columns to drop to record pairs of correlated features
    #     corr_record = pd.DataFrame()
    #     for column in tqdm(to_drop, 'Correlation DataFrame'):
    #         cond = upper[column] > threshold
    #         corr_features = list(upper.index[cond])  # Find the correlated features
    #         corr_values = list(upper[column][cond])  # Find the correlated values
    #         drop_features = [column for _ in range(len(corr_features))]
    #         df_tmp = pd.DataFrame({'drop_feature': drop_features,
    #                                'corr_feature': corr_features,
    #                                'corr_value': corr_values})
    #         corr_record = corr_record.append(df_tmp, ignore_index=True, sort=False)
    #
    #     self.corr_record = corr_record
    #     print('%d features with a  correlation coefficient greater than %0.2f.' % (len(to_drop), threshold))
    #
    # @property
    # def to_drop_all(self):
    #     return self.to_drop_missing + self.to_drop_unique + self.to_drop_variance + self.to_drop_correlation + self.to_drop_zero_importance + self.to_drop_low_importance
