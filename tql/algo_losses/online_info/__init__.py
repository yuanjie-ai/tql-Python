"""
auc表示（正样本概率>负样本概率）的概率 # 可以算期望

根据线上auc猜测正负样本数
1/正样本数 = 2 * auc - 1  # gini = 2 * auc - 1 与gini公式一致
如果auc<0.5就是负样本数

预测错的个数 > (1 - auc) * 正样本数 
# 至少 (1 - auc) * 正样本数 未召回
# 至多有 auc * 正样本数 召回 准确率不超过 auc
"""

"""f1
提交一个正确的正样本(确保f1不为0)得到线上f1
猜一个1其他全为0: 正样本数 = 2 / f1 - 1
猜一个0其他全为1: 正样本数 = (总样本数 - 1) / (2 / f1 - 1)  # 概率更大
"""

"""acc
猜一个1其他全为0: 正样本数 = 总样本数 * acc - 1
猜一个0其他全为1: 负样本数 = 总样本数 * acc - 1
"""


def result_scaling(x=0.37, rate_train_true=0.37, rate_test_true=0.165):
    """根据log_loss缩放结果，适用于线上线下样本分布不一致
    Refer:
    https://www.kaggle.com/c/quora-question-pairs/discussion/31179
    https://www.kaggle.com/badat0202/estimate-distribution-of-data-in-lb
    """
    a = rate_test_true / rate_train_true
    b = (1 - rate_test_true) / (1 - rate_train_true)
    scale_pos_weight = a / b  # 利用scale_pos_weight缩放结果
    print("Xgb/Lgb scale_pos_weight: %s" % scale_pos_weight)
    return a * x / (a * x + b * (1 - x))


def get_weight(y):
    class_weight = dict(enumerate(len(y) / (2 * np.bincount(y))))
    sample_weight = [class_weight[i] for i in y]
    return class_weight, sample_weight