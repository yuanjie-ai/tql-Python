[<h1 align = "center">:rocket: 特征选择 :facepunch:</h1>][1]

---
https://github.com/duxuhao/Feature-Selection
---
## 目标
- 提高预测的准确性
- 构造更快，消耗更低的预测模型
- 能够对模型有更好的理解和解释

---
## 1. Fillter
- 去除低方差的特征
- 单变量特征选择：F检验仅捕获线性依赖性、互信息可以捕捉变量之间的任何依赖关系
    - 对于回归: f_regression , mutual_info_regression
    - 对于分类: chi2 , f_classif , mutual_info_classif

---
## 2. Wrapper
- [递归（特征子集）特征选择][2]
    - RFE
    - RFECV
- 树模型特征选择

---
## 3. Embeded
- L1特征选择
  - `from sklearn.svm import LinearSVC`

---
## 4. Genetic
- [sklearn-genetic][3]

---
- 降噪编码器
- 各种降维技术

---
[1]: https://www.cnblogs.com/stevenlk/p/6543628.html
[2]: https://github.com/Jie-Yuan/DataMining/edit/master/3_FeatureEngineering/3_FeatureSelection/RFE.md
[3]: https://github.com/manuel-calzolari/sklearn-genetic
