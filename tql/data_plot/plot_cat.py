#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'plot_cat'
__author__ = 'JieYuan'
__mtime__ = '2019-04-26'
"""
import seaborn as sns
import matplotlib.pyplot as plt


def plot_count(df, cat='rentType', figsize=(9, 4), title='Title'):
    """饼图+计数直方图"""
    f, ax = plt.subplots(1, 2, figsize=figsize)
    plt.suptitle(title)
    plt.subplots_adjust(left=None, bottom=None, right=None, top=None, wspace=0.5, hspace=None)
    df[cat].value_counts().plot.pie(autopct='%1.2f%%', ax=ax[0], shadow=True)
    sns.countplot(cat, data=df, ax=ax[1])
    for _ax in ax:
        _ax.set_title(cat)
    plt.show()


def distplot(data, x, y, figsize=(20, 8)):
    """
    g = sns.FacetGrid(train, col='rentType')
    g.map(sns.distplot, 'tradeMoney', bins=20)
    g.map(plt.hist, 'tradeMoney', bins=20)
    """
    cats = data[x].unique()
    f, ax = plt.subplots(1, len(cats), sharey=True, figsize=figsize)
    for cat, _ax in zip(cats, ax):
        _ax.set_title(cat)
        sns.distplot(data[y][data[x] == cat], ax=_ax)
    plt.show()

#
# # sns.heatmap(data.corr(),annot=True,cmap='RdYlGn',linewidths=0.2) #data.corr()-->correlation matrix
# # fig=plt.gcf()
# # fig.set_size_inches(10,8)
# # plt.show()
# # sns.heatmap(train.astype(float).corr(),linewidths=0.1,vmax=1.0,
# #             square=True, cmap=colormap, linecolor='white', annot=True)
#
#
# pd.crosstab([train.houseFloor, train.rentType], train.houseDecoration, margins=True) \
#     .style.background_gradient(cmap='summer_r')
#
# # grid = sns.FacetGrid(train_df, col='Pclass', hue='Survived')
# grid = sns.FacetGrid(train, col='houseFloor', row='rentType', aspect=1.6)
# grid.map(plt.hist, 'tradeMoney', alpha=.5, bins=20)
# grid.add_legend();
