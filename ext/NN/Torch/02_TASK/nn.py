# encoding: utf-8
import torch
import numpy as np

def gen_data(num=1000):
    x = torch.unsqueeze(torch.linspace(-1, 1, num), dim=1)  # x data (tensor), shape=(100, 1)
    y = x.pow(2) + 0.2 * torch.rand(x.size())
    y = y.mean(0)
    return x.squeeze(), y
class Net(torch.nn.Module):
    def __init__(self):
        super(Net,self).__init__()
        self.hidden=torch.nn.Linear(1000,10)
        self.predict=torch.nn.Linear(10,1)
    def forward(self,x):
        out=self.hidden(x)
        out=self.predict(out)
        return out

def train(x,y):
    net=Net()
    optimizer = torch.optim.SGD(net.parameters(), lr=0.01)
    for epoch in range(100):
        out=net(x)
        l=(out-y)*(out-y)
        optimizer.zero_grad()
        l.backward()
        optimizer.step()
        print("progress", epoch, l.data)
    out = net(x)
    l = (out - y) * (out - y)
    print(l.data)

if __name__ == '__main__':
    x, y = gen_data()
    train(x,y)