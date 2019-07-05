# encoding: utf-8

from xplan import *
from xplan.models.classifier import BaselineLGB
from sklearn.feature_selection import SelectKBest, mutual_info_classif, chi2

train = pd.read_csv('train.csv', lineterminator='\n')
test = pd.read_csv('test.csv', lineterminator='\n')

y = train.label.replace({'Positive': 1, 'Negative': 0})
data = train.append(test).drop('label', 1)

tfidf = TfidfVectorizer(lowercase=True, ngram_range=(1, 5), max_features=6000)
tfidf_mat = tfidf.fit_transform(data.review)

X = tfidf_mat[:6328]
X_test = tfidf_mat[6328:]

X1 = SelectKBest(chi2, 1000).fit_transform(X, y) # 0.791
X2 = SelectKBest(mutual_info_classif, 1000).fit_transform(X, y) # 0.787

b = BaselineLGB(X1, y)
b.run()

b = BaselineLGB(X2, y)
b.run()