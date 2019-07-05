[<h1 align = "center">:rocket: Bagging :facepunch:</h1>][1]

---
> Bootstraping，即自助法：它是一种有放回的抽样方法（可能抽到重复的样本）

## Bagging (bootstrap aggregating)

Bagging即套袋法，其算法过程如下：

A）从原始样本集中抽取训练集。每轮从原始样本集中使用Bootstraping的方法抽取n个训练样本（在训练集中，有些样本可能被多次抽取到，而有些样本可能一次都没有被抽中）。共进行k轮抽取，得到k个训练集。（k个训练集之间是相互独立的）

B）每次使用一个训练集得到一个模型，k个训练集共得到k个模型。（注：这里并没有具体的分类算法或回归方法，我们可以根据具体问题采用不同的分类或回归方法，如决策树、感知器等）

C）对分类问题：将上步得到的k个模型采用投票的方式得到分类结果；对回归问题，计算上述模型的均值作为最后的结果。（所有模型的重要性相同）

![bagging][2]
---
[1]: http://blog.csdn.net/good_boyzq/article/details/54730004
[2]: http://img.blog.csdn.net/20170208160930513
