[<h1 align = "center">:rocket: 熵 :facepunch:</h1>][0]

---
## 信息熵、联合熵、条件熵、信息增益的关系：

![熵、联合熵、条件熵、互信息的关系][5]

---
- 信息：I(x)用来表示随机变量的信息，p(xi)指是当xi发生时的概率

![信息][3]

- 熵：表示随机变量的不确定性（度量系统无序程度），越有序熵越小，越无序熵越大（参照概率分布理解）

- 信息熵：考虑该随机变量的所有可能取值，即所有可能发生事件所带来的信息量的期望

![信息熵][1]

- 条件熵：在一个条件下，随机变量的不确定性。定义为X给定条件下，Y的条件概率分布的熵对X的数学期望

![条件熵][2]

- 信息增益(互信息)

![信息增益][4]

- 信息增益比(Infomation Gain Ratio)：gr = IG(Y|X)/H(X)

- Gini系数：一种与信息熵类似的做特征选择的方式，可以用来数据的不纯度（加入特征X以后，数据不纯度减小的程度越大说明特征X越重要）

> 在决策树算法中，ID3使用信息增益，C4.5使用信息增益比，CART使用Gini系数。

- 联合熵
- 交叉熵（类比信息熵）

![交叉熵][6]

- 相对熵（KL散度）：KL散度/距离是衡量两个分布的距离（信息熵 - 交叉熵）

![KL][7]

https://mp.weixin.qq.com/s/jH1OkNwgxiSeqQw6VTFU1A

---
[0]: http://blog.csdn.net/haolexiao/article/details/70142571
[1]: https://pic2.zhimg.com/80/v2-a9f081eff039a7e65f51515d4aacb34b_hd.jpg
[2]: https://pic2.zhimg.com/80/v2-f925bd0dba2f4584ebd78efea6c9864c_hd.jpg
[3]: https://images0.cnblogs.com/blog2015/605905/201506/161909021542396.png
[4]: http://images0.cnblogs.com/blog2015/605905/201506/162013009355725.png
[5]: https://images2015.cnblogs.com/blog/788753/201610/788753-20161027151210843-745348026.png
[6]: http://img.blog.csdn.net/20170907162730719
[7]: http://colah.github.io/posts/2015-09-Visual-Information/img/CrossEntropyQP.png
