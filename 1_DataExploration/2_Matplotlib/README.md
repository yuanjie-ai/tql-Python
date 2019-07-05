<h1 align = "center">:rocket: Matplotlib :facepunch:</h1>

---
### 常用参数
- 坐标轴：
    - 范围：xlim/ylim
    - 刻度：xticks/yticks
    - 角度：rot
    - 变换坐标轴：
        - secondary_y
        - use_index
- 基本属性：
    - 位置：layout
    - 标题：title
    - 大小：figsize
	- 图例：legend
```
%matplotlib inline
import matplotlib.pyplot as plt
plt.style.use('ggplot')

# 中文乱码的处理
plt.rcParams['font.sans-serif'] =['Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False
```

- 'line' : line plot (default)
- 'bar' : vertical bar plot
- 'barh' : horizontal bar plot
- 'hist' : histogram
- 'box' : boxplot
- 'kde' : Kernel Density Estimation plot
- 'density' : same as 'kde'
- 'area' : area plot
- 'pie' : pie plot
- 'scatter' : scatter plot
- 'hexbin' : hexbin plot


---
## [Matplotlib][0]
- [matplotlib(条形图)][1]
- [matplotlib(饼图)][2]
- [matplotlib(箱线图)][3]
- [matplotlib(直方图)][4]
- [matplotlib(折线图)][5]
- [matplotlib(散点图)][6]
- [matplotlib(雷达图)][7]
- [matplotlib(面积图)][8]
- [matplotlib(热力图)][9]
- [matplotlib(树地图)][10]
---
[1]: https://mp.weixin.qq.com/s?__biz=MzIxNjA2ODUzNg==&mid=2651435778&idx=1&sn=df430bcbaf2b285b47bdaf3fa6168405&chksm=8c73abd5bb0422c3c1b15639d63eb8677163a54f314059959edbe5340a19411ac8fcdd4f0f61&scene=21#wechat_redirect
[2]: https://mp.weixin.qq.com/s?__biz=MzIxNjA2ODUzNg==&mid=2651435782&idx=1&sn=56283c740c5f7b091abbde874061ece6&chksm=8c73abd1bb0422c720915adc56cc21b46a3433526946e82357f01799c0c6bc954bc756f42122&scene=21#wechat_redirect
[3]: https://mp.weixin.qq.com/s?__biz=MzIxNjA2ODUzNg==&mid=2651435787&idx=1&sn=f79ba08a1a0da7574fdf9fde4376b697&chksm=8c73abdcbb0422ca0f5ccc76e67032c13cc0c960ba921449b8c0da8bf55c0deb1b353c06ee63&scene=21#wechat_redirect
[4]: https://mp.weixin.qq.com/s?__biz=MzIxNjA2ODUzNg==&mid=2651435794&idx=1&sn=7dc745b1c4a732af1a05fdc7fb008f26&chksm=8c73abc5bb0422d35468036de663bb62abfaf04aca9224af0b5f028f3febf78b5c3f876733a4&scene=21#wechat_redirect
[5]: https://mp.weixin.qq.com/s?__biz=MzIxNjA2ODUzNg==&mid=2651435807&idx=1&sn=788a8baee32b69ad181a06557642ed2a&chksm=8c73abc8bb0422de3319686c3ea8b8fcc8bf9786e4ece52d063afe54ecbdcfa230623dfeb4b1&scene=21#wechat_redirect
[6]: https://mp.weixin.qq.com/s?__biz=MzIxNjA2ODUzNg==&mid=2651435814&idx=1&sn=c12e3113023f05e0cfafe637401923d6&chksm=8c73abf1bb0422e7c86f30de8249d53ed4b7d1be6bf7f52abc26d28985b40a48e330176d4d4b&scene=21#wechat_redirect
[7]: https://mp.weixin.qq.com/s/FnKnDk_e6PzVxyiJkyrnpg
[8]: https://mp.weixin.qq.com/s/neQTcJhTCl60vDOaHcElHQ
[9]: https://mp.weixin.qq.com/s/L8TYeAknyLG4mzVYyMSiEw
[10]: https://mp.weixin.qq.com/s/KiElfDtrkfJu8eIyYNu3Dw

[0]: http://nbviewer.jupyter.org/github/Jie-Yuan/2_DataMining/blob/master/1_DataExploration/2_Matplotlib/1_Matplotlib.ipynb
