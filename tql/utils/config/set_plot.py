#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : plot_set
# @Time         : 2019-06-20 11:28
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import matplotlib.pyplot as plt


def set_plot():
    """
    plt.rcParams['font.sans-serif'] = ['Simhei']  # 中文乱码的处理
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False  # 负号
    plt.rcParams["text.usetex"] = False
    plt.rcParams["legend.numpoints"] = 1
    plt.rcParams["figure.figsize"] = (18, 9)  # (12, 6)
    plt.rcParams["figure.dpi"] = 128
    plt.rcParams["savefig.dpi"] = plt.rcParams["figure.dpi"]
    plt.rcParams["font.size"] = 12
    plt.rcParams["pdf.fonttype"] = 42
    """
    plt.rcParams['font.sans-serif'] = ['Simhei']  # 中文乱码的处理
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['axes.unicode_minus'] = False  # 负号
    plt.rcParams["text.usetex"] = False
    plt.rcParams["legend.numpoints"] = 1
    plt.rcParams["figure.figsize"] = (18, 9)  # (12, 6)
    plt.rcParams["figure.dpi"] = 128
    plt.rcParams["savefig.dpi"] = plt.rcParams["figure.dpi"]
    plt.rcParams["font.size"] = 12
    plt.rcParams["pdf.fonttype"] = 42
    print('Setting Success!')
