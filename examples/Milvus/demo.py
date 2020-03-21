#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : demo
# @Time         : 2020-02-14 11:52
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : https://github.com/milvus-io/docs/blob/master/site/en/guides/milvus_operation.md#createdrop-indexes-in-a-collection
# TODO:
# m.milvus.preload_table

import sys
import numpy as np
import random
from milvus import Milvus, IndexType, MetricType
import time


class MilvusANN(object):

    def __init__(self, host='10.46.5.98', port='19530'):
        self.milvus = Milvus()

        print("Client Version:", self.milvus.client_version())

        status = self.milvus.connect(host, port)

        if status.OK():
            print("Server connected.")
        else:
            print("Server connect fail.")
            sys.exit(1)

        print("Server Version:", self.milvus.server_version()[-1])

    def desc(self, tabel_name=None):
        milvus = self.milvus
        milvus.show_collections()
        # milvus.drop_collection()
        if tabel_name:
            print(f"Describe: {milvus.describe_collection(tabel_name)[-1]}")
            print(f"Vector number in {tabel_name}: {milvus.count_collection(tabel_name)}")

    def create_tabel_demo(self):
        # Create table demo_table if it dosen't exist.
        milvus = self.milvus
        table_name = 'demo_table'

        status, ok = milvus.has_collection(table_name)
        if not ok:
            param = {
                'collection_name': table_name,
                'dimension': 16,
                'index_file_size': 1024,  # optional index_file_size：文件到达这个大小的时候，milvus开始为这个文件创建索引。
                'metric_type': MetricType.L2  # optional
            }

            milvus.create_collection(param)

        # Show tables in Milvus server
        _, collections = milvus.show_collections()

        # Describe demo_table
        _, table = milvus.describe_collection(table_name)
        print(table)

    def insert_vectors_demo(self, collection_name):
        milvus = self.milvus

        # 10000 vectors with 16 dimension
        # element per dimension is float32 type
        # vectors should be a 2-D array
        # vectors = [[random.random() for _ in range(16)] for _ in range(10000)]
        vectors = np.random.rand(10000, 16).astype(np.float32).tolist()
        # You can also use numpy to generate random vectors:
        #     `vectors = np.random.rand(10000, 16).astype(np.float32).tolist()`

        # Insert vectors into demo_table, return status and vectors id list
        status, self.ids = milvus.insert(collection_name, vectors)  # 时间戳 1581655102 786 118

        # Wait for 6 seconds, until Milvus server persist vector data.
        time.sleep(6)

        # Get demo_table row count
        status, result = milvus.count_collection(collection_name)

        # create index of vectors, search more rapidly
        index_param = {
            'nlist': 2048
        }

        # Create ivflat index in demo_table
        # You can search vectors without creating index. however, Creating index help to
        # search faster
        status = milvus.create_index(collection_name, index_type=IndexType.IVFLAT, params=index_param)

        # describe index, get information of index
        status, index = milvus.describe_index(collection_name)
        print(index)

        # Use the top 10 vectors for similarity search
        self._query_vectors = vectors[0:10]

    def search_vectors_demo(self, query_vectors, collection_name):
        milvus = self.milvus

        # execute vector similarity search
        status, results = milvus.search_vectors(collection_name,
                                                top_k=1,
                                                query_records=query_vectors,
                                                params={'nprobe': 16})
        if status.OK():
            # indicate search result
            # also use by:
            #   `results.distance_array[0][0] == 0.0 or results.id_array[0][0] == ids[0]`
            if results[0][0].distance == 0.0 or results[0][0].id == self.ids[0]:
                print('Query result is correct')
            else:
                print('Query result isn\'t correct')

        # print results
        print(results)

    def drop_table(self, collection_name):
        milvus = self.milvus

        # Delete demo_table
        status = milvus.drop_collection(collection_name)

        # Disconnect from Milvus
        status = milvus.disconnect()


if __name__ == '__main__':
    MilvusANN()
