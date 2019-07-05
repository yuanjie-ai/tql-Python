import numpy as np
import math
from scipy.linalg import norm
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer

# 依赖包numpy、python-Levenshtein、scipy

# euclidean,欧式距离算法，传入参数为两个向量，返回值为欧式距离
def Euclidean(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    return math.sqrt(((npvec1-npvec2)**2).sum())


# Manhattan_Distance,曼哈顿距离
def Manhattan(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    return np.abs(npvec1-npvec2).sum()


# Chebyshev_Distance,切比雪夫距离
def Chebyshev(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    return max(np.abs(npvec1-npvec2))


# MinkowskiDistance 闵可夫斯基距离，其实就是上面三种距离的集合，这里就不重复了。
def Minkowski(vec1, vec2, params):
    pass

# def Standardized_Euclidean(vec1, vec2, v):
#     from scipy import spatial
#     npvec = np.array([np.array(vec1), np.array(vec2)])
#     return spatial.distance.pdist(npvec, 'seuclidean', V=None)
# Standardized Euclidean distance,标准化欧氏距离
# 在对长方体区域进行聚类的时候，普通的距离无法满足要求。
# 按照普通的距离聚类出的大多是圆形的区域，这时候要采用标准的欧式距离。
# 参考  标准化欧式距离：http://blog.csdn.net/jinzhichaoshuiping/article/details/51019473

# 马氏距离，优点：去除量纲，而且可以排除变量之间的相关性的干扰
x1 = [3, 5, 2]
x2 = [4, 6, 2]
x3 = [6,7,2]
x4 = [10,1,7]
def mahalanobis(*args, v1=None, v2=None): # v1,v2包含在args中
    X = np.vstack(args).T
    S = np.cov(X)
    SI = np.linalg.inv(S)
    return np.dot(np.dot((v1 - v2).T, SI), (v1 - v2))
print(mahalanobis([x1,x2,x3,x4],v1=x1,v2=x2))

# Cosine，余弦夹角
# 机器学习中借用这一概念来衡量样本向量之间的差异。
def Cosine(vec1, vec2):
    npvec1, npvec2 = np.array(vec1), np.array(vec2)
    return npvec1.dot(npvec2)/(math.sqrt((npvec1**2).sum()) * math.sqrt((npvec2**2).sum()))


################################################################################################
#-------------------------------------文本相似度算法-------------------------------------------#

# 针对列表改写的编辑距离，在NLP领域中，计算两个文本的相似度，是基于句子中词和词之间的差异。
# 如果使用传统的编辑距离算法，则计算的为文本中字与字之间的编辑次数。这里根据编辑距离的思维，
# 将编辑距离中的处理字符串中的字符对象，变成处理list中每个元素
def Edit_distance_array(str_ary1, str_ary2):
    len_str_ary1 = len(str_ary1) + 1
    len_str_ary2 = len(str_ary2) + 1
    matrix = [0 for n in range(len_str_ary1 * len_str_ary2)]
    for i in range(len_str_ary1):
        matrix[i] = i
    for j in range(0, len(matrix), len_str_ary1):
        if j % len_str_ary1 == 0:
            matrix[j] = j // len_str_ary1
    for i in range(1, len_str_ary1):
        for j in range(1, len_str_ary2):
            if str_ary1[i-1] == str_ary2[j-1]:
                cost = 0
            else:
                cost = 1
            matrix[j*len_str_ary1+i] = min(matrix[(j-1)*len_str_ary1+i]+1, matrix[j*len_str_ary1+(i-1)]+1, matrix[(j-1)*len_str_ary1+(i-1)] + cost)
    distance = int(matrix[-1])
    similarity = 1-int(matrix[-1])/max(len(str_ary1), len(str_ary2))
    return {'Distance': distance, 'Similarity': similarity}

# 余弦相似度算法
# 算法一 基于句子的TF
def cosine_similarity_tf(s1, s2):
    """
    计算两个句子的TF余弦相似度
    :param s1:
    :param s2:
    :return:
    """
    vectorizer = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = vectorizer.fit_transform(corpus).toarray()
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

# 算法二 基于句子的TFIDF
def cosine_similarity_tfidf(s1, s2):
    """
    计算两个句子的TFIDF余弦相似度
    :param s1:
    :param s2:
    :return:
    """
    vectorizer = TfidfVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = vectorizer.fit_transform(corpus).toarray()
    return np.dot(vectors[0], vectors[1]) / (norm(vectors[0]) * norm(vectors[1]))

# WMD距离
# https://blog.csdn.net/cht5600/article/details/53405315
from gensim.similarities import WmdSimilarity

# Jaccard距离
def jaccard_similarity(s1, s2):
    """
    计算两个句子的雅可比相似度
    :param s1:
    :param s2:
    :return:
    """
    vectorizer = CountVectorizer(tokenizer=lambda s: s.split())
    corpus = [s1, s2]
    vectors = vectorizer.fit_transform(corpus).toarray()
    numerator = np.sum(np.min(vectors, axis=0))
    denominator = np.sum(np.max(vectors, axis=0))
    return 1.0 * numerator / denominator
