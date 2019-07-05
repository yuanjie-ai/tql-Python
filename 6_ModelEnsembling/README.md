[<h1 align = "center">:rocket: Ensemble Learning :facepunch:</h1>][0]

---
## 1. 结合策略
- 平均法
- 投票法
    - 硬投票：每个模型输出它自认为最可能的类别，投票模型从其中选出投票模型数量最多的类别，作为最终分类。
    - 软投票：每个模型输出一个所有类别的概率矢量(1 * n_classes)，投票模型取其加权平均，得到一个最终的概率矢量。
- 学习法：Stacking

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
[0]: http://www.cnblogs.com/jasonfreak/p/5657196.html
