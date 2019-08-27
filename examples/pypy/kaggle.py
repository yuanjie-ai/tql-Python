#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : kaggle
# @Time         : 2019-08-27 13:37
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from tqdm import tqdm
from csv import DictReader

import json
from tqdm import tqdm
from csv import DictReader


def csv2libffm(input, fieldnames=None, cols_cat=None, cols_num=None, cols_multi_cat=None, label='label', sep=',',
               output='train.libffm', features_map='features.json'):
    global field_features
    field_features = {}
    dialect_map = {',': 'excel', '\t': 'excel-tab'}
    with open(output, 'a') as output:
        with open(input) as input:
            for row in tqdm(DictReader(input, fieldnames, dialect=dialect_map[sep]), desc="Transform ..."):
                line = []

                # 类别型
                cols_cat = cols_cat if cols_cat else [i for i in row.keys() if i != label]  # 默认全部为 类别型
                for idx, field in enumerate(cols_cat, 1):
                    feature = row[field]
                    ff = field + '______' + feature if feature else 'NA'  # 类别值就是一个 bin
                    fnum = field_features.setdefault(ff, len(field_features) + 1)

                    line.append(f'{idx}:{fnum}:1')

                # 多类别型： TODO: cols_multi_cat

                # 数值型
                if cols_num is not None:
                    for idx, field in enumerate(cols_num, idx + 1):
                        feature = row[field]
                        ff = field  # 数值当作一个 bin
                        fnum = field_features.setdefault(ff, len(field_features) + 1)

                        if feature != '' and feature != '0':
                            line.append(f'{idx}:{fnum}:{feature}')

                output.write(f"{row.get(label, '-1')} {' '.join(line)}\n")


    with open(features_map, 'w') as f:
        return json.dump(field_features, f)

if __name__ == '__main__':
    csv2libffm('/Users/yuanjie/train.csv', label='HasDetections', output='train_.libffm')