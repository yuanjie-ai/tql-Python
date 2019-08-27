#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'fm_data'
__author__ = 'JieYuan'
__mtime__ = '2019/4/4'
"""
"""
https://www.cnblogs.com/wkang/p/9788012.html
https://blog.csdn.net/songbinxu/article/details/79662665
"""
import os
from collections import defaultdict
from csv import DictReader
import math


class DF2FFM(object):

    def __init__(self):
        pass

    def transform(self, input, output, exclude, excluse):
        pass

train_path = '../input/train.csv'

dont_use = ['MachineIdentifier',
            'Census_FirmwareVersionIdentifier',
            'Census_OEMModelIdentifier',
            'CityIdentifier']

cols_num = []
cols_cat = []
cols_multi_cat = []
# 大值平滑
too_many_vals = ["Census_PrimaryDiskTotalCapacity",
                 "Census_SystemVolumeTotalCapacity",
                 "Census_TotalPhysicalRAM",
                 "Census_InternalPrimaryDiagonalDisplaySizeInInches",
                 "Census_InternalPrimaryDisplayResolutionHorizontal",
                 "Census_InternalPrimaryDisplayResolutionVertical",
                 "Census_InternalBatteryNumberOfCharges"]

categories = [k for k, v in dtypes.items() if k not in dont_use]
categories_index = dict(zip(categories, range(len(categories))))

field_features = defaultdict()

max_val = 1
with open('train.libffm', 'a') as the_file:
    for t, row in enumerate(DictReader(open(train_path))):
        if t % 100000 == 0:
            print(t, len(field_features), max_val)
        label = [row['HasDetections']]
        ffeatures = []

        for field in categories:
            if field == 'HasDetections':
                continue
            feature = row[field]
            if feature == '':
                feature = "unk"
            if field not in num_cols:
                ff = field + '_____' + feature
            else:
                if feature == "unk" or float(feature) == -1:
                    ff = field + '_____' + str(0)
                else:
                    if field in too_many_vals:
                        ff = field + '_____' + str(int(round(math.log(1 + float(feature)))))
                    else:
                        ff = field + '_____' + str(int(round(float(feature))))

            if ff not in field_features:
                if len(field_features) == 0:
                    field_features[ff] = 1
                    max_val += 1
                else:
                    field_features[ff] = max_val + 1
                    max_val += 1

            fnum = field_features[ff]

            ffeatures.append('{}:{}:1'.format(categories_index[field], fnum))
        line = label + ffeatures
        the_file.write('{}\n'.format(' '.join(line)))
