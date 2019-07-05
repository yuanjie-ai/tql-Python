
torch.Tensor.view # Returns a new tensor with the same data as the self tensor but of a different shape.
torch.Tensor.reshape


主要是针对model 在训练时和评价时不同的 Batch Normalization  和  Dropout 方法模式。
model.train()
model.eval()，让model变成测试模式，对dropout和batch normalization的操作在训练和测试的时候是不一样的

