# encoding: utf-8
import torch
import numpy as np
lr=0.001
def gen_data(num=1000):
    """""
    y = 3*x1+4*x2
    """""
    x1 = np.linspace(0, 9, num)
    x2 = np.linspace(4, 13, num)
    x = np.concatenate(([x1], [x2]), axis=0).T
    y = np.dot(x, np.array([3, 4]).T)
    x = torch.from_numpy(x)
    y = torch.from_numpy(y)
    return x, y
def loss(y_pred,y):
    loss=(y_pred-y)*(y_pred-y)
    return loss.mean()
def sdg(x,y):
    w = torch.autograd.Variable(torch.DoubleTensor(2,1).zero_(),requires_grad=True)
    print(x.shape)
    print(w.shape)

    for epoch in range(100):
        l=loss(x.mm(w).squeeze(1),y)
        l.backward(torch.ones_like(l))
        print("grad",w.grad.data[0])
        w.data=w.data-lr*w.grad.data
        w.grad.data.zero_()
        print("progress:", epoch, l.data)
    print(w)
if __name__ == '__main__':
    x, y = gen_data()
    sdg(x,y)