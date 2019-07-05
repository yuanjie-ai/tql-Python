# encoding: utf-8
"""https://blog.csdn.net/Kaiyuan_sjtu/article/details/80030005"""
from xplan import *
from xplan.models import OOF

import pandas as pd

from sklearn.naive_bayes import GaussianNB
from sklearn.svm import SVC, NuSVC, LinearSVC

train = pd.read_csv('train.csv', lineterminator='\n')
test = pd.read_csv('test.csv', lineterminator='\n')

y = train.label.replace({'Positive': 1, 'Negative': 0})
data = train.append(test).drop('label', 1)

tfidf = TfidfVectorizer(lowercase=True, ngram_range=(1, 3), max_features=6000)
tfidf_mat = tfidf.fit_transform(data.review)

X = tfidf_mat[:6328]  # .toarray()
X_test = tfidf_mat[6328:]  # .toarray()

# pipeline = make_pipeline(QuantileTransformer(output_distribution='normal'), GaussianNB())
#
# OOF(pipeline).fit(X, y, X_test)
# OOF(GaussianNB()).fit(X, y, X_test)

OOF(LinearSVC()).fit(X, y, X_test)
# for clf in SVC(), NuSVC(), LinearSVC():
#     OOF(clf).fit(X, y, X_test)
