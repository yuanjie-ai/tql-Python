<h1 align = "center">:rocket: 模型融合 :facepunch:</h1>

---

## 1. 结合策略
- 平均法
- 投票法
    - 硬投票：uses predicted class labels for majority rule voting
	- 软投票：predicts the class label based on the argmax of the sums of the predicted probalities
- 学习法

---
## 2. 多样性
- 误差——分歧分解
- 多样性度量
- 多样性增强
    - 数据样本扰动
    - 输入属性扰动
    - 算法参数扰动
    - 输出表示扰动
        - 翻转法(Flipping Output)：随机改变一些训练样本标记
        - 输出调制法(Output Smearing)：分类输出转化为回归输出
        - OVO/ECOC

---
