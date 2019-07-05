https://github.com/bresan/entity_embeddings_categorical

https://www.tensorflow.org/guide/feature_columns#categorical_identity_column


# [偏离值特征][1]
偏离值特征指单个个体与分组之间的偏离距离。以下的代码所生成的特征便是这一类特征：
首先，根据分组字段对数据集进行分组
然后计算每个个体与分组的均值、最小值、最大值和求和值之间的偏离距离


---
[1]: https://shawnyxiao.github.io/2018/02/07/%E3%80%90%E6%95%B0%E6%8D%AE%E6%8C%96%E6%8E%98%E6%AF%94%E8%B5%9B%E3%80%91%E4%BC%81%E4%B8%9A%E7%BB%8F%E8%90%A5%E9%80%80%E5%87%BA%E9%A3%8E%E9%99%A9%E9%A2%84%E6%B5%8B/#more