<h1 align = "center">:rocket: EDA :facepunch:</h1>

---
## 1. [Missingno][1]: [Demo][3]

---
## 2. [Seaborn][2]
```python
sns.heatmap(corrMatrix.ix[:10, :10], center=0, annot=True, annot_kws={'size': 10}, fmt='.2f', square=True)
sns.clustermap(corrMatrix.ix[:10, :10], fmt="d",cmap='YlGnBu')
```
---
## 初始化设置
```python
import matplotlib.pyplot as plt
class Matplotlib(object):
    def __init__(self):
        """
        https://www.programcreek.com/python/example/4890/matplotlib.rcParams
        """
        pass

    def init_matplotlib(self):
        """初始化设置"""
        plt.style.use('ggplot')
        plt.rcParams['font.sans-serif'] = ['Microsoft YaHei'] # 中文乱码的处理
        plt.rcParams['axes.unicode_minus'] = False # 负号
        plt.rcParams["text.usetex"] = False
        plt.rcParams["legend.numpoints"] = 1
        plt.rcParams["figure.figsize"] = (10, 5)
        plt.rcParams["figure.dpi"] = 100
        plt.rcParams["savefig.dpi"] = plt.rcParams["figure.dpi"]
        plt.rcParams["font.size"] = 10
        plt.rcParams["pdf.fonttype"] = 42

    def clear_state(self):
        plt.close('all')
        plt.rcdefaults()
```

---
## 色系
xx
![色系][4]










---
[1]: https://github.com/ResidentMario/missingno
[2]: https://github.com/Jie-Yuan/2_DataMining/tree/master/1_DataExploration/3_Seaborn
[3]: https://github.com/Jie-Yuan/DataMining/blob/master/1_DataExploration/4_Missingno/README.md
[4]: http://image.sciencenet.cn/album/201205/24/174610e77x998p3s3wy9p8.png

