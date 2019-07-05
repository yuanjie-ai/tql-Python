# -*- coding: utf-8 -*-
import ffm
from tqdm import tqdm

class FFM(object):
    _model = None
    def __init__(self, eta=0.1, l2=0.00002, factor=4, n_iter=15):
        '''
        :param eta: set learning rate
        :param l2: set regularization parameter
        :param factor: set number of latent factors
        :param n_iter: set number of iterations
        '''
        self.eta = eta
        self.l2 = l2
        self.factor = factor
        self.n_iter = n_iter

    @staticmethod
    def FFMData(X, y):
        '''
        prepare the data
        :param X: (field, index, value) format
        :param y:
        :return:
        '''
        return ffm.FFMData(X, y)

    def fit(self, X, y):
        '''
        :param X: (field, index, value) format
        :param y: 0 or 1
        :return:
        '''
        ffm_data = ffm.FFMData(X, y)
        model = ffm.FFM(self.eta, self.l2, self.factor)
        model.init_model(ffm_data)
        for i in tqdm(range(self.n_iter)):
            model.iteration(ffm_data)
        FFM._model = model
        return model

    @classmethod
    def predict(cls, X, y):
        ffm_data = ffm.FFMData(X, y)
        return cls._model.predict(ffm_data)

    @classmethod
    def save_model(cls, path):
        cls._model.save_model(path)
        return 'save model'

# X = [[(1, 2, 1), (2, 3, 1), (3, 5, 1)],
#      [(1, 0, 1), (2, 3, 1), (3, 7, 1)],
#      [(1, 1, 1), (2, 3, 1), (3, 7, 1), (3, 9, 1)],]
# 
# y = [1, 1, 0]
# _ffm = FFM()
# _ffm.fit(X, y)
# _ffm.predict(X, y)
