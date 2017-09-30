<h1 align = "center">:rocket: 基于最小描述长度的最优分箱 :facepunch:</h1>

- 性能测试
```
import time
start = time.time()
data = pd.read_csv('F:\\JieYuan\\2_WorkProject\\data.csv')
for i in range(15):
    data = data.append(data, ignore_index=True)
print(data.shape)
discretizer = MDLP_Discretizer(dataset=data,
                               class_label='e',
                               out_path_data='F:\\JieYuan\\2_WorkProject\\data_log.csv',
                               out_path_bins='F:\\JieYuan\\2_WorkProject\\bin_log.txt' )
print(start - time.time())
```
```
(3276800, 5)
F:\JieYuan\2_WorkProject\data_log.csv
-63.04100012779236
```

- out_path_data

|a|b|c|d|e|e|
|:--:|:--:|:--:|:--:|:--:|:--:|
|5.05_to_5.15|3.45_to_inf|-inf_to_2.45|-inf_to_0.8|0.0|0.0|
|4.85_to_5.05|2.95_to_3.05|-inf_to_2.45|-inf_to_0.8|0.0|0.0|
|-inf_to_4.85|3.05_to_3.35|-inf_to_2.45|-inf_to_0.8|0.0|0.0|
|-inf_to_4.85|3.05_to_3.35|-inf_to_2.45|-inf_to_0.8|0.0|0.0|
|4.85_to_5.05|3.45_to_inf|-inf_to_2.45|-inf_to_0.8|0.0|0.0|
|5.35_to_5.45|3.45_to_inf|-inf_to_2.45|-inf_to_0.8|0.0|0.0|
|-inf_to_4.85|3.35_to_3.45|-inf_to_2.45|-inf_to_0.8|0.0|0.0|
|4.85_to_5.05|3.35_to_3.45|-inf_to_2.45|-inf_to_0.8|0.0|0.0|
|-inf_to_4.85|2.85_to_2.95|-inf_to_2.45|-inf_to_0.8|0.0|0.0|
|4.85_to_5.05|3.05_to_3.35|-inf_to_2.45|-inf_to_0.8|0.0|0.0|

- out_path_bins
```
Description of bins in file: F:\JieYuan\2_WorkProject\data_log.csv
attr: a
	-inf_to_4.85, 4.85_to_5.05, 5.05_to_5.15, 5.15_to_5.25, 5.25_to_5.35, 5.35_to_5.45, 5.45_to_5.55, 5.55_to_5.65, 5.65_to_5.85, 5.85_to_inf
attr: b
	-inf_to_2.25, 2.25_to_2.35, 2.35_to_2.85, 2.85_to_2.95, 2.95_to_3.05, 3.05_to_3.35, 3.35_to_3.45, 3.45_to_inf
attr: c
	-inf_to_2.45, 2.45_to_inf
attr: d
	-inf_to_0.8, 0.8_to_inf

```
