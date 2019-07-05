# -*- coding: utf-8 -*-
"""
__title__ = 'hive'
__author__ = 'JieYuan'
__mtime__ = '18-11-19'
"""


class Hive(object):
    get_feats = lambda feats: [i.split('.')[1] if '.' in i else i for i in feats]

    def gen_cols(self, feats_str: list = [], feats_num: list = [], all_feats: list = []):
        if all_feats:
            if feats_str or feats_num:
                if feats_str:
                    z = zip(range(1024), ['string' if feat in feats_str else 'double' for feat in all_feats], all_feats)
                else:
                    z = zip(range(1024), ['double' if feat in feats_num else 'string' for feat in all_feats], all_feats)

            res = '\n'.join([f"{idx}:optional {dtype} {feat};//{feat}" for idx, dtype, feat in z])
        else:
            z = zip(range(1024), len(feats_str) * ['string'] + len(feats_num) * ['double'], feats_str + feats_num)
            res = '\n'.join([f"{idx}:optional {dtype} {feat};//{feat}" for idx, dtype, feat in z])
        print(res)

    def gen_agg_cols(self, feats: list, funcs: list = None):
        """
        :param column: str
        :param funcs: list or tuple
            'mean', 'max', 'min', ...
            mad skew kurt待增加
        :return:
        """
        exprs = lambda column: {
            'sum': f'AVG({column}) AS {column}_sum',
            'mean': f'AVG({column}) AS {column}_mean',
            'max': f'MAX({column}) AS {column}_max',
            'min': f'MIN({column}) AS {column}_min',
            'range': f'MAX({column}) - MIN({column}) AS {column}_range',
            'std': f'STDDEV_SAMP({column}) AS {column}_std',
            'per25': f'PERCENTILE_APPROX({column}, 0.25) AS {column}_per25',
            'per50': f'PERCENTILE_APPROX({column}, 0.50) AS {column}_per50',
            'per75': f'PERCENTILE_APPROX({column}, 0.75) AS {column}_per75',
            'iqr': f'PERCENTILE_APPROX({column}, 0.75) - PERCENTILE_APPROX({column}, 0.25) AS {column}_iqr',
            'cv': f'STDDEV_SAMP({column}) / (AVG({column}) + pow(10, -8)) AS {column}_cv',
            'zeros_num': f'COUNT(CASE WHEN {column} = 0 THEN 1 ELSE NULL END) AS {column}_zeros_num',
            'zeros_perc': f'COUNT(CASE WHEN {column} = 0 THEN 1 ELSE NULL END) / COUNT(1) AS {column}_zeros_perc'
        }

        if funcs is None:
            res = ',\n'.join([',\n'.join(exprs(feat).values()) for feat in feats])
        else:
            assert isinstance(funcs, tuple) or isinstance(funcs, list)
            res = ',\n'.join([',\n'.join([exprs(feat)[func] for func in funcs]) for feat in feats])
        print(res)
