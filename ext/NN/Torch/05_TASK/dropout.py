# encoding: utf-8
import numpy as np
from torch import nn
class Dropout():

    def __init__(self, prob=0.5):
        self.prob = prob
        self.params = []

    def forward(self, X):
        self.mask = np.random.binomial(1, self.prob, size=X.shape) / self.prob
        out = X * self.mask
        return out.reshape(X.shape)

    def backward(self, dout):
        dX = dout * self.mask
        return dX, []

# dropout numpy实现
def dropout(x, p):
    # 测试时需要乘的1-p
    retain_prob = 1 - p
    # 利用binomial函数，生成与x一样的维数向量。
    # 神经元x保留的概率为p，n表示每个神经元参与随机实验的次数，通常为1,。
    # size是神经元总数。
    sample=np.random.binomial(n=1,p=retain_prob,size=x.shape)
    # 生成一个0、1分布的向量，0表示该神经元被丢弃
    # print sample
    x *=sample
    # 规范化
    x /= retain_prob
    return x


# pytorch中dropout的实现,在非线性层之后加了随机失活层
F.dropout(input, p=0.5, training=False, inplace=False)
# 任务四改进：
class MyClassifier(nn.Module):
    def __init__(self):
        super(MyClassifier,self).__init__()
        self.fc1 = nn.Linear(2,4)
        self.fc2 = nn.Linear(4,6)
        self.fc3 = nn.Linear(6,3)
        self.fc4 = nn.Linear(3,2)
    def forward(self,x):
        x = self.fc1(x)
        a1 = F.tanh(x)
        x = F.dropout(a1,p=0.5)
        x = self.fc2(a1)
        a2 = F.tanh(x)
        x = F.dropout(a2,p=0.5)
        x = self.fc3(a2)
        a3 = F.relu(x)
        x = F.dropout(a3,p=0.5)
        x = self.fc4(x)
        return a1,a2,a3,x