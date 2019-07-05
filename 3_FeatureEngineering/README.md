<h1 align = "center">:rocket: 特征工程 :facepunch:</h1>

---
待总结干货：
http://m.sohu.com/a/139981834_116235

https://www.cnblogs.com/5poi/p/7240601.html
---
## 特征加法
- [Categorical encoding][11]
    - [count_encoder][12]
    - LeaveOneOutEncoder
    - TargetEncoder
    - BaseNEncoder: http://www.willmcginnis.com/2016/12/18/basen-encoding-grid-search-category_encoders/
    - OneHotEncoder, 
    - BinaryEncoder,
    - OrdinalEncoder, 
    - HashingEncoder
    - SumEncoder, 
    - HelmertEncoder,
    - PolynomialEncoder, 
    - BackwardDifferenceEncoder, 
    - forward difference encoding, 
    - combination of any of these encodings, self-made encodings
    - 遗传编码https://www.kaggle.com/aharless/logistic-of-genetic-features/notebook
- Linear combination of features (ex: v1+v2, 0.132882*v1+95.4294829428*v2...)
- ICA
- PLS
- Positive Rates
- Negative Rates
- Canonical Correlation
- Box-Cox transformation
- Yeo-Johnson transformation
- Normalization
- Standardization
- Discretization of continuous features (many methods existing)
- Model output
- Tree output (features coming from a tree model)
- Wide&Deep

---
## 特征提取(傻瓜式)
- [featuretools][3]: https://mp.weixin.qq.com/s/1Zj_pQDBqBJKSrtt9HsKXg
- DAE等
- GBDT
- [spherical k-means][5]
- 时间序列
    - [tsfresh][6]
    - [fbprophet][7]
    - [pyflux][8]
    
http://blog.csdn.net/qq_37195507/article/details/78590637

## 特征选择
- [scikit-feature][4]
- SequentialFeatureSelector
---
## [常用特征变换][0]

```
# 参数要满足：
# if (df_out and (sparse or default)):
#     raise ValueError("Can not use df_out with sparse or default")
```
---
## [缺失值特征工程][9]
- missingno
---
## 类别型特征
- [类编码][1]: [category_encoders][2]
---
## 数值型特征
- 映射平滑
  - 移动平均法
  - 指数平滑
  - 对数平滑
  - [贝叶斯平滑][20]
  - 拉普拉斯平滑
- [Box-Cox][21]
---
## 特征重要性
---
## 特征衍生技巧
- 统计特征
- 分离特征: 时间戳属性通常分离成模型需要的多个维度比如年、月、日、小时、分钟、秒钟
- 交叉特征: 不同特征群之间的交叉特征，比如UI交互特征


---
[网友的一些总结][10]















---
[0]: http://nbviewer.jupyter.org/github/Jie-Yuan/2_DataMining/blob/master/3_FeatureEngineering/sklearn_pandas.ipynb
[1]: http://contrib.scikit-learn.org/categorical-encoding/backward_difference.html
[2]: https://github.com/scikit-learn-contrib/categorical-encoding
[3]: https://github.com/Featuretools/featuretools
[4]: https://github.com/jundongl/scikit-feature
[5]: https://github.com/justinsalamon/skm
[6]: https://github.com/blue-yonder/tsfresh
[7]: https://github.com/facebook/prophet
[8]: http://pyflux.readthedocs.io/en/latest/arima.html
[9]: https://github.com/Jie-Yuan/DataMining/tree/master/3_FeatureEngineering/missingno
[10]: http://www.cnblogs.com/weibao/p/6252280.html
[11]: https://github.com/Jie-Yuan/DataMining/tree/master/3_FeatureEngineering/1_CategoricalEncoding
[12]: https://github.com/Jie-Yuan/DataMining/blob/master/3_FeatureEngineering/1_CategoricalEncoding/count_encoder.py

[20]: https://github.com/Jie-Yuan/2_DataMining/blob/master/3_FeatureEngineering/SmoothMapping/BayesianSmoothing.py
[21]: http://nbviewer.jupyter.org/github/Jie-Yuan/2_DataMining/blob/master/3_FeatureEngineering/Box-Cox/Box-Cox.ipynb
