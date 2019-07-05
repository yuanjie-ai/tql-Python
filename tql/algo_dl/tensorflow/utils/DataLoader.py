#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
__title__ = 'DataLoader'
__author__ = 'JieYuan'
__mtime__ = '19-3-22'
"""
import tensorflow as tf
import pandas as pd


class DataLoader(object):

    def __init__(self, X: pd.DataFrame, y=None, batch_size=128):
        self.X = dict(X)
        self.y = y
        self.batch_size = batch_size

    def train_input_fn(self):
        """An input function for training
        https://www.tensorflow.org/alpha/tutorials/estimators/boosted_trees
        """
        inputs = (self.X, self.y)

        # Convert the inputs to a Dataset.
        dataset = tf.data.Dataset.from_tensor_slices(inputs)

        # Shuffle, repeat, and batch the examples.
        dataset = dataset.shuffle(1000).repeat().batch(self.batch_size)

        # Return the dataset.
        return dataset

    def eval_input_fn(self):
        """An input function for evaluation or prediction"""
        if self.y is None:
            # No labels, use only features.
            inputs = self.X
        else:
            inputs = (self.X, self.y)

        # Convert the inputs to a Dataset.
        dataset = tf.data.Dataset.from_tensor_slices(inputs)

        # Batch the examples
        dataset = dataset.batch(self.batch_size)

        # Return the dataset.
        return dataset


if __name__ == '__main__':
    from tensorflow_estimator import estimator
    from sklearn.datasets import load_iris

    tf.get_logger().setLevel(2)

    CSV_COLUMN_NAMES = ['SepalLength', 'SepalWidth',
                        'PetalLength', 'PetalWidth']  # 'Species'
    X, y = load_iris(True)
    X = pd.DataFrame(X, columns=CSV_COLUMN_NAMES)

    # Feature columns describe how to use the input.
    my_feature_columns = list(map(tf.feature_column.numeric_column, CSV_COLUMN_NAMES))

    clf = estimator.DNNClassifier(hidden_units=[10, 10],
                                  feature_columns=my_feature_columns,
                                  n_classes=3,
                                  batch_norm=True)

    clf = estimator.BoostedTreesClassifier(feature_columns=my_feature_columns,
                                           n_batches_per_layer=2,
                                           n_classes=2,
                                           n_trees=100,
                                           max_depth=6,
                                           learning_rate=0.1,
                                           l1_regularization=0.,
                                           l2_regularization=0.,
                                           tree_complexity=0.,
                                           min_node_weight=0.,
                                           center_bias=False,
                                           pruning_mode='none',
                                           quantile_sketch_epsilon=0.01)

    clf.train(DataLoader(X[:100], y[:100], 64).train_input_fn, steps=1000)

    predict_x = {
        'SepalLength': [5.1, 5.9, 6.9],
        'SepalWidth': [3.3, 3.0, 3.1],
        'PetalLength': [1.7, 4.2, 5.4],
        'PetalWidth': [0.5, 1.5, 2.1],
    }

    print(list(clf.predict(DataLoader(predict_x).eval_input_fn)))
