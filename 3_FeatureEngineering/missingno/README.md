## 基于缺失值的特征工程
在对缺失值进行分析时，我们发现一部分特征的缺失情况之间存在关联，如下图所示：
![missingno.heatmap(collisions)][1]

- ps_ind_02_cat与ps_ind_04_cat、ps_car_01_cat，这三个变量的缺失情况在彼此之间的相关性很强。
- 其中，ps_car_01_cat与ps_ind_04_cat的缺失情况相关性是所有系数里最高的。我们可以猜测，这三列之间具有一定的相关关系，使得一旦其中有一个变量出现缺失，其余两个变量的缺失与否也会受到影响。
- 此外，ps_car_07_cat和ps_ind_05_cat这两列的缺失情况之间也具有很强的相关性。
- ps_03_cat和ps_05_cat的缺失情况之间同样具有很高的相关性，但是如果考虑到这两列的缺失值都非常的多，就可以认为这是很理所当然的

### 基于此，尝试构筑以下三个特征：http://blog.csdn.net/qq_37195507/article/details/78590637
- MissingTotal_1：样本在ps_ind_02_cat、ps_ind_04_cat、ps_car_01_cat这三个特征出现缺失值的个数之和。 
- MissingTotal_2：样本在ps_car_07_cat和ps_ind_05_cat这两个特征中出现缺失值的个数之和。 
- MissingTotal_3：样本在ps_car_03_cat和ps_car_05_cat这两个特征中出现缺失值的个数之和。














---
[1]: http://img.blog.csdn.net/20171121094452337?watermark/2/text/aHR0cDovL2Jsb2cuY3Nkbi5uZXQvcXFfMzcxOTU1MDc=/font/5a6L5L2T/fontsize/400/fill/I0JBQkFCMA==/dissolve/70/gravity/SouthEast
