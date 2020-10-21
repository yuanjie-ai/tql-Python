#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : reverse_metrics
# @Time         : 2020/9/8 4:46 下午
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


def get_num_pos_neg(num_sample, online_metric, metric='auc'):
    if metric == 'auc':
        """
        猜一个1其他全为0: 如果得分小于0.5说明猜错了，也就是该样本为负样本
        """
        num_pos = 1 / (2 * online_metric - 1)
        if num_pos < 0:
            num_pos += num_sample

    elif metric == 'f1':
        """f1
        提交一个正确的正样本(确保f1不为0)得到线上f1
        猜一个1其他全为0: 正样本数 = 2 / f1 - 1
        猜一个0其他全为1: 正样本数 = (总样本数 - 1) / (2 / f1 - 1)  # 概率更大
        猜错得分为0，猜对得分都大于0
        """
        # 猜 0
        num_pos = (num_sample - 1) / (2 / online_metric - 1)
        # # 猜 1
        # num_pos = 2 / online_metric - 1

    num_neg = num_sample - num_pos
    num_pos, num_neg = map(round, [num_pos, num_neg])

    print(f"num_pos/num_neg = {num_pos}/{num_neg} = 1/{num_neg / num_pos}")


def reverse_f1(reversed_f1, num_pos_pred, num_pos_true, num_neg_true):
    """

    :param reversed_f1: 反向f1
    :param num_pos_true:
    :param num_neg_true:
    :param num_pos_pred: 反向就是原来预测的负样本数，也就是提交的正样本数
    :return:
    """
    # 命中个数
    z = num_pos_true - f2 * (num_pos_true + num_pos_pred) / 2
    print(f'命中个数: {z}')

    f1_true = 2 * z / (num_pos_true + num_pos_true + num_neg_true - num_pos_pred)

    return f1_true
