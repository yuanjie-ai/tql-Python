#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = '__init__.py'
__author__ = 'JieYuan'
__mtime__ = '19-1-30'
"""
from .WordCloud import WordCloud
from .chinese_setting import chinese_setting

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


def plot_feature_importances(features, importances, topk=20, figsize=(10, 6)):
    columns = ['Importances', 'Features']
    df = pd.DataFrame(list(zip(importances, features)), columns=columns).sort_values('Importances', 0, False)

    plt.figure(figsize=figsize)
    sns.barplot(*columns, data=df[:topk])
    plt.title('Features Importances\n')
    plt.tight_layout()
    plt.savefig('lgbm_importances.png')
