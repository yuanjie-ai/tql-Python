#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-Python.
# @File         : pytorch
# @Time         : 2020-02-10 12:54
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


from torch.utils import data
from tqdm import tqdm
from skorch.helper import SliceDict


class MyDataset(data.Dataset):
    def __init__(self, filepath, transformer=str.strip):
        self.number = None
        self.filepath = filepath
        self.transformer = transformer
        self.__file = open(self.filepath, "r")
        # pd.read_csv(csv_file, iterator=True).get_chunk(128).as_matrix().astype('float')

        # 可爱的进度条
        with open(filepath, "r") as f:
            for self.number, _ in tqdm(enumerate(f, 1), desc="load data ..."):
                pass

    def __len__(self):
        return self.number

    def __getitem__(self, index):
        _ = self.__file.__next__()
        _ = self.transformer(_)
        return _


train_dataset = MyDataset(filepath="train.txt")
training_data = data.DataLoader(dataset=train_dataset, batch_size=32, num_workers=1, shuffle=True)
