# encoding: utf-8
import torch
def l1_penalty(var):
    return torch.abs(var).sum()


def l2_penalty(var):
    return torch.sqrt(torch.pow(var, 2).sum())


torch.optim.SGD # weight_decay表示l2正则