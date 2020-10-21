# coding: utf-8
__title__ = 'Entropy'
__author__ = 'JieYuan'
__mtime__ = '2017/9/29'


import pandas as pd
import numpy as np
from math import log
import random


def entropy(data_classes, base=2):
    '''
    Computes the entropy of a set of labels (class instantiations)
    :param base: logarithm base for computation
    :param data_classes: Series with labels of examples in a dataset
    :return: value of entropy
    '''
    if not isinstance(data_classes, pd.core.series.Series):
        raise AttributeError('input array should be a pandas_utils series')
    classes = data_classes.unique()
    N = len(data_classes)
    ent = 0  # initialize entropy

    # iterate over classes
    for c in classes:
        partition = data_classes[data_classes == c]  # data with class = c
        proportion = len(partition) / N
        #update entropy
        ent -= proportion * log(proportion, base)

    return ent

def cut_point_information_gain(dataset, cut_point, feature_label, class_label):
    '''
    Return de information gain obtained by splitting a numeric attribute in two according to cut_point
    :param dataset: pandas_utils dataframe with a column for attribute values and a column for class
    :param cut_point: threshold at which to partition the numeric attribute
    :param feature_label: column label of the numeric attribute values in data
    :param class_label: column label of the array of instance classes
    :return: information gain of partition obtained by threshold cut_point
    '''
    if not isinstance(dataset, pd.core.frame.DataFrame):
        raise AttributeError('input dataset should be a pandas_utils data frame')

    entropy_full = entropy(dataset[class_label])  # compute entropy of full dataset (w/o split)

    #split data at cut_point
    data_left = dataset[dataset[feature_label] <= cut_point]
    data_right = dataset[dataset[feature_label] > cut_point]
    (N, N_left, N_right) = (len(dataset), len(data_left), len(data_right))

    gain = entropy_full - (N_left / N) * entropy(data_left[class_label]) - \
        (N_right / N) * entropy(data_right[class_label])

    return gain

# from sklearn.datasets import load_iris
# iris = load_iris()
# X, y = iris.data[:100], iris.target[:100]
# df = pd.DataFrame(np.hstack([X, y.reshape(-1, 1)]), columns=list('abcde'))
# for i in np.arange(df.a.min(), df.a.max(), 0.01):
#     print(i, cut_point_information_gain(df, i, 'a', 'e')) # i=5.5 熵最大？？？

# python PyTest.py --in_path='F:\\JieYuan\\2_WorkProject\\data.csv' --out_path='F:\\JieYuan\\2_WorkProject' --class_label=e
