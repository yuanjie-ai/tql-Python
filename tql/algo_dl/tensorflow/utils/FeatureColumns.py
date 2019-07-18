#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'FeatureColumns'
__author__ = 'JieYuan'
__mtime__ = '19-3-22'
"""
import tensorflow as tf

"""
https://blog.csdn.net/u014061630/article/details/82937333
https://www.tensorflow.org/beta/tutorials/keras/feature_columns
https://github.com/tensorflow/tensorflow/issues/27416
"""

# 数值列
# 分桶列
_ = tf.feature_column.numeric_column(key='Year')
tf.feature_column.bucketized_column(source_column=_, boundaries=[1960, 1980, 2000])

# 分类标识列
tf.feature_column.categorical_column_with_identity(key='my_feature_b', num_buckets=4)  # Values [0, 4)

# 分类词汇列：分类标识列的枚举版本（多了一步词到数值映射）
tf.feature_column.categorical_column_with_vocabulary_list(key='feat1',
                                                          vocabulary_list=["kitchenware", "electronics", "sports"])
tf.feature_column.categorical_column_with_vocabulary_file(key='feat1',
                                                          vocabulary_file='./cats.txt')

# 经过哈希处理的列
# tf.feature_column.categorical_column_with_hash_bucket(key=_,
#                                                       hash_buckets_size=10)  # The number of categories
# 组合列
# https://developers.google.com/machine-learning/glossary/#feature_cross
# https://www.tensorflow.org/guide/feature_columns#crossed_column
tf.feature_column.crossed_column(['latitude_bucket_fc', 'longitude_bucket_fc'], 5000)  # using 5000 hash bins.

# 指标列和嵌入列
# tf.feature_column.indicator_column()  # one-hot
# tf.feature_column.embedding_column(categorical_column=categorical_column, dimension=embedding_dimensions)


# if __name__ == '__main__':
#     # 低阶 api
#     features = {
#         'sales': [[5], [10], [8], [9]],
#         'department': ['sports', 'sports', 'gardening', 'gardening']}
#
#     department_column = tf.feature_column.categorical_column_with_vocabulary_list(
#         'department', ['sports', 'gardening'])
#     department_column = tf.feature_column.indicator_column(department_column)
#
#     columns = [
#         tf.feature_column.numeric_column('sales'),
#         department_column
#     ]
#
#     inputs = tf.feature_column.input_layer(features, columns)
#     var_init = tf.global_variables_initializer()
#     table_init = tf.tables_initializer()
#
#     with tf.Session() as sess:
#         sess.run((var_init, table_init))
#         print(sess.run(inputs))
