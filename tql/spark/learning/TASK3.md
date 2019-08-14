# Task3

内容：DataFrame,SparkSQL

第4章

[4.1 Spark SQL简介](http://dblab.xmu.edu.cn/blog/1717-2/)

[4.2 DataFrame与RDD的区别](http://dblab.xmu.edu.cn/blog/1718-2/)

[4.3 DataFrame的创建](http://dblab.xmu.edu.cn/blog/1719-2/)

[4.4 从RDD转换得到DataFrame](http://dblab.xmu.edu.cn/blog/1720-2/)

[4.5.2 通过JDBC连接数据库(DataFrame)](http://dblab.xmu.edu.cn/blog/1724-2/)

第5章

[5.1 流计算简介](http://dblab.xmu.edu.cn/blog/1732-2/)

[5.2 Spark Streaming简介](http://dblab.xmu.edu.cn/blog/1733-2/)

第5.3节 DStream操作

[5.3.1 DStream操作概述](http://dblab.xmu.edu.cn/blog/1737-2/)

问题扩展：请简述下spark sql的运行机制。
---

Spark SQL 原理和运行机制

[Catalyst 执行优化器](https://link.jianshu.com?t=http://pengshuang.space/2017/02/07/Spark实践-3-Spark-SQL-与数据仓库/#Catalyst-执行优化器)

Catalyst 是 Spark SQL 执行优化器的代号，所有 Spark SQL 语句最终都能通过它来解析、优化，最终生成可以执行的 Java 字节码。

Catalyst 最主要的数据结构是树，所有 SQL 语句都会用树结构来存储，树中的每个节点有一个类（class），以及 0 或多个子节点。Scala 中定义的新的节点类型都是 TreeNode 这个类的子类。

Catalyst 另外一个重要的概念是规则。基本上，所有优化都是基于规则的。可以用规则对树进行操作，树中的节点是只读的，所以树也是只读的。规则中定义的函数可能实现从一棵树转换成一颗新树。

整个 Catalyst 的执行过程可以分为以下 4 个阶段：

分析阶段，分析逻辑树，解决引用

逻辑优化阶段

物理计划阶段，Catalyst 会生成多个计划，并基于成本进行对比

代码生成阶段

 catalyst整体执行流程

说到spark sql不得不提的当然是Catalyst了。Catalyst是spark sql的核心，是一套针对spark sql 语句执行过程中的查询优化框架。因此要理解spark sql的执行流程，理解Catalyst的工作流程是理解spark sql的关键。而说到Catalyst，就必须得上下面这张图1了，这张图描述了spark sql执行的全流程。其中，长方形框内为catalyst的工作流程。



![img](https:////upload-images.jianshu.io/upload_images/2119554-6cb9890d54a53ef4.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/546/format/webp)



图1 spark sql 执行流程图

SQL语句首先通过Parser模块被解析为语法树，此棵树称为Unresolved Logical Plan；Unresolved Logical Plan通过Analyzer模块借助于Catalog中的表信息解析为Logical Plan；此时，Optimizer再通过各种基于规则的优化策略进行深入优化，得到Optimized Logical Plan；优化后的逻辑执行计划依然是逻辑的，并不能被Spark系统理解，此时需要将此逻辑执行计划转换为Physical Plan。

**Catalyst工作流程**

任何一个优化器工作原理都大同小异：SQL语句首先通过Parser模块被解析为语法树，此棵树称为Unresolved Logical Plan；Unresolved Logical Plan通过Analyzer模块借助于数据元数据解析为Logical Plan；此时再通过各种基于规则的优化策略进行深入优化，得到Optimized Logical Plan；优化后的逻辑执行计划依然是逻辑的，并不能被Spark系统理解，此时需要将此逻辑执行计划转换为Physical Plan；为了更好的对整个过程进行理解，下文通过一个简单示例进行解释。

**Parser**

Parser简单来说是将SQL字符串切分成一个一个Token，再根据一定语义规则解析为一棵语法树。Parser模块目前基本都使用第三方类库ANTLR进行实现，比如Hive、 Presto、SparkSQL等。下图是一个示例性的SQL语句（有两张表，其中people表主要存储用户基本信息，score表存储用户的各种成绩），通过Parser解析后的AST语法树如右图所示：





![img](https:////upload-images.jianshu.io/upload_images/9129747-e5861ad2c1c352b6.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/953/format/webp)



**Analyzer**

通过解析后的逻辑执行计划基本有了骨架，但是系统并不知道score、sum这些都是些什么鬼，此时需要基本的元数据信息来表达这些词素，最重要的元数据信息主要包括两部分：表的Scheme和基本函数信息，表的scheme主要包括表的基本定义（列名、数据类型）、表的数据格式（Json、Text）、表的物理位置等，基本函数信息主要指类信息。

Analyzer会再次遍历整个语法树，对树上的每个节点进行数据类型绑定以及函数绑定，比如people词素会根据元数据表信息解析为包含age、id以及name三列的表，people.age会被解析为数据类型为int的变量，sum会被解析为特定的聚合函数，如下图所示：

SparkSQL中Analyzer定义了各种解析规则，有兴趣深入了解的童鞋可以查看Analyzer类，其中定义了基本的解析规则，如下：





![img](https:////upload-images.jianshu.io/upload_images/9129747-58987d44bbdf0c02.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/965/format/webp)



**Optimizer**



![img](https:////upload-images.jianshu.io/upload_images/9129747-3cb65da900d749ef.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/683/format/webp)



优化器是整个Catalyst的核心，上文提到优化器分为基于规则优化和基于代价优化两种，当前SparkSQL 2.1依然没有很好的支持基于代价优化（下文细讲），此处只介绍基于规则的优化策略，基于规则的优化策略实际上就是对语法树进行一次遍历，模式匹配能够满足特定规则的节点，再进行相应的等价转换。因此，基于规则优化说到底就是一棵树等价地转换为另一棵树。SQL中经典的优化规则有很多，下文结合示例介绍三种比较常见的规则：谓词下推（Predicate Pushdown）、常量累加（Constant Folding）和列值裁剪（Column Pruning）。



![img](https:////upload-images.jianshu.io/upload_images/9129747-cf227fe1be40e532.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/925/format/webp)



上图左边是经过Analyzer解析后的语法树，语法树中两个表先做join，之后再使用age>10对结果进行过滤。大家知道join算子通常是一个非常耗时的算子，耗时多少一般取决于参与join的两个表的大小，如果能够减少参与join两表的大小，就可以大大降低join算子所需时间。谓词下推就是这样一种功能，它会将过滤操作下推到join之前进行，上图中过滤条件age>0以及id!=null两个条件就分别下推到了join之前。这样，系统在扫描数据的时候就对数据进行了过滤，参与join的数据量将会得到显著的减少，join耗时必然也会降低。





![img](https:////upload-images.jianshu.io/upload_images/9129747-04cf4b26df3cab0e.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/916/format/webp)



常量累加其实很简单，就是上文中提到的规则  x+(1+2)  -> x+3，虽然是一个很小的改动，但是意义巨大。示例如果没有进行优化的话，每一条结果都需要执行一次100+80的操作，然后再与变量math_score以及english_score相加，而优化后就不需要再执行100+80操作。

列值裁剪是另一个经典的规则，示例中对于people表来说，并不需要扫描它的所有列值，而只需要列值id，所以在扫描people之后需要将其他列进行裁剪，只留下列id。这个优化一方面大幅度减少了网络、内存数据量消耗，另一方面对于列存数据库（Parquet）来说大大提高了扫描效率。



![img](https:////upload-images.jianshu.io/upload_images/9129747-b1ef19c961b4c270.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/893/format/webp)



除此之外，Catalyst还定义了很多其他优化规则，有兴趣深入了解的童鞋可以查看Optimizer类，下图简单的截取一部分规则：





![img](https:////upload-images.jianshu.io/upload_images/9129747-781924b6b8fd127a.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/877/format/webp)



至此，逻辑执行计划已经得到了比较完善的优化，然而，逻辑执行计划依然没办法真正执行，他们只是逻辑上可行，实际上Spark并不知道如何去执行这个东西。比如Join只是一个抽象概念，代表两个表根据相同的id进行合并，然而具体怎么实现这个合并，逻辑执行计划并没有说明。



![img](https:////upload-images.jianshu.io/upload_images/9129747-d1d806d38437ff5f.png?imageMogr2/auto-orient/strip%7CimageView2/2/w/877/format/webp)



此时就需要将逻辑执行计划转换为物理执行计划，将逻辑上可行的执行计划变为Spark可以真正执行的计划。比如Join算子，Spark根据不同场景为该算子制定了不同的算法策略，有BroadcastHashJoin、ShuffleHashJoin以及SortMergeJoin等（可以将Join理解为一个接口，BroadcastHashJoin是其中一个具体实现），物理执行计划实际上就是在这些具体实现中挑选一个耗时最小的算法实现，这个过程涉及到基于代价优化策略，后续文章细讲。