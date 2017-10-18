<h1 align = "center">:rocket: 特征工程 :facepunch:</h1>

---
## [常用特征变换][0]
```
# 参数要满足：
# if (df_out and (sparse or default)):
#     raise ValueError("Can not use df_out with sparse or default")
``
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

[10]: http://www.cnblogs.com/weibao/p/6252280.html

[20]: https://github.com/Jie-Yuan/2_DataMining/blob/master/3_FeatureEngineering/SmoothMapping/BayesianSmoothing.py
[21]: http://nbviewer.jupyter.org/github/Jie-Yuan/2_DataMining/blob/master/3_FeatureEngineering/Box-Cox/Box-Cox.ipynb
