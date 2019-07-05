- 有时数据会分散在几个不同的文件中，需要 Join 起来。
- 处理 Missing Data。
- 处理 Outlier。
- 必要时转换某些 Categorical Variable 的表示方式。
- 有些 Float 变量可能是从未知的 Int 变量转换得到的，这个过程中发生精度损失会在数据中产生不必要的 Noise，即两个数值原本是相同的却在小数点后某一位开始有不同。这对 Model 可能会产生很负面的影响，需要设法去除或者减弱 Noise。
- 当一个变量从直觉上来说对所要完成的目标有帮助，就可以将其作为 Feature.至于它是否有效，最简单的方式就是通过图表来直观感受。
- 通过挑选出最重要的 Feature，可以将它们之间进行各种运算和操作的结果作为新的 Feature，可能带来意外的提高。


```
常见的 Ensemble 方法有这么几种：

Bagging：使用训练数据的不同随机子集来训练每个 Base Model，最后进行每个 Base Model 权重相同的 Vote。也即 Random Forest 的原理。
Boosting：迭代地训练 Base Model，每次根据上一个迭代中预测错误的情况修改训练样本的权重。也即 Gradient Boosting 的原理。比 Bagging 效果好，但更容易 Overfit。
Blending：用不相交的数据训练不同的 Base Model，将它们的输出取（加权）平均。实现简单，但对训练数据利用少了。
Stacking：接下来会详细介绍。

从理论上讲，Ensemble 要成功，有两个要素：

Base Model 之间的相关性要尽可能的小。这就是为什么非 Tree-based Model 往往表现不是最好但还是要将它们包括在 Ensemble 里面的原因。Ensemble 的 Diversity 越大，最终 Model 的 Bias 就越低。
Base Model 之间的性能表现不能差距太大。这其实是一个 Trade-off，在实际中很有可能表现相近的 Model 只有寥寥几个而且它们之间相关性还不低。但是实践告诉我们即使在这种情况下 Ensemble 还是能大幅提高成绩。
```


---
- 特征选择
https://www.kaggle.com/tilii7/boruta-feature-elimination

https://www.kaggle.com/ogrellier/feature-selection-with-null-importances



---