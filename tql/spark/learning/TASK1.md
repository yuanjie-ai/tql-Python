# 【task 1 环境部署】

[window下参考](https://blog.csdn.net/SummerHmh/article/details/89518567)

[linux下参考1](https://mp.weixin.qq.com/s/gIf_QGQL26MqMzZKk-YTLg)

[linux下参考2](https://mp.weixin.qq.com/s/vufnqfG1vYjT9Ec8kvjcAg)

内容：运行原理，RDD设计，DAG，安装与使用

第1章 Spark的设计与运行原理（大概了解）

[1.1 Spark简介](http://dblab.xmu.edu.cn/blog/1710-2/)

[1.2 Spark运行架构](http://dblab.xmu.edu.cn/blog/1711-2/)

[1.3 RDD的设计与运行原理](http://dblab.xmu.edu.cn/blog/1681-2/)

- [1.4 Spark的部署模式](http://dblab.xmu.edu.cn/blog/1713-2/)

第2章 Spark的安装与使用（主要内容）

- [2.1 Spark的安装和使用](http://dblab.xmu.edu.cn/blog/1689-2/) （如果想在window上安装，[参考](https://blog.csdn.net/SummerHmh/article/details/89518567)，之后可以用pyspark或者jupyter上进行学习）

- 2.2 第一个Spark应用程序：[WordCount](./word_count.py)

问题扩展：

1. spark 和 mapreduce有哪些区别，请用具体的例子说明？[参考](https://blog.csdn.net/wyz0516071128/article/details/81219342)

   - MapReduce存在的问题

   1. MapReduce框架局限性

   　　1）仅支持Map和Reduce两种操作

   　　2）处理效率低效。

   　　　　a）Map中间结果写磁盘，Reduce写HDFS，多个MR之间通过HDFS交换数据; 任务调度和启动开销大;

   　　　　b）无法充分利用内存

   　　　　c）Map端和Reduce端均需要排序

   　　3）不适合迭代计算(如机器学习、图计算等)，交互式处理(数据挖掘) 和流式处理(点击日志分析)

   2. MapReduce编程不够灵活

   　　1）尝试scala函数式编程语言

   - Spark

   1. 高效(比MapReduce快10~100倍)

   　　1）内存计算引擎，提供Cache机制来支持需要反复迭代计算或者多次数据共享，减少数据读取的IO开销

   　　2）DAG引擎，减少多次计算之间中间结果写到HDFS的开销

   　　3）使用多线程池模型来减少task启动开稍，shuffle过程中避免 不必要的sort操作以及减少磁盘IO操作

   2. 易用

   　　1）提供了丰富的API，支持Java，Scala，Python和R四种语言

   　　2）代码量比MapReduce少2~5倍

   3. 与Hadoop集成 读写HDFS/Hbase 与YARN集成 

2. rdd的本质是什么？[参考](https://www.cnblogs.com/deadend/p/6710468.html)

   一个RDD就是一个分布式对象集合，本质上是一个只读的分区记录集合，每个RDD可以分成多个分区，每个分区就是一个数据集片段，并且一个RDD的不同分区可以被保存到集群中不同的节点上，从而可以在集群中的不同节点上进行并行计算。RDD提供了一种高度受限的共享内存模型，即RDD是只读的记录分区的集合，不能直接修改，只能基于稳定的物理存储中的数据集来创建RDD，或者通过在其他RDD上执行确定的转换操作（如map、join和groupBy）而创建得到新的RDD。RDD提供了一组丰富的操作以支持常见的数据运算，分为“行动”（Action）和“转换”（Transformation）两种类型，前者用于执行计算并指定输出的形式，后者指定RDD之间的相互依赖关系。两类操作的主要区别是，转换操作（比如map、filter、groupBy、join等）接受RDD并返回RDD，而行动操作（比如count、collect等）接受RDD但是返回非RDD（即输出一个值或结果）。RDD提供的转换接口都非常简单，都是类似map、filter、groupBy、join等粗粒度的数据转换操作，而不是针对某个数据项的细粒度修改。因此，RDD比较适合对于数据集中元素执行相同操作的批处理式应用，而不适合用于需要异步、细粒度状态的应用，比如Web应用系统、增量式的网页爬虫等。正因为这样，这种粗粒度转换接口设计，会使人直觉上认为RDD的功能很受限、不够强大。但是，实际上RDD已经被实践证明可以很好地应用于许多并行计算应用中，可以具备很多现有计算框架（比如MapReduce、SQL、Pregel等）的表达能力，并且可以应用于这些框架处理不了的交互式数据挖掘应用。