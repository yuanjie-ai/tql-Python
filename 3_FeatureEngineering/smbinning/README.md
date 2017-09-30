
```
data = pd.read_csv('F:\\JieYuan\\2_WorkProject\\data.csv')
for i in range(10):
    data = data.append(data, ignore_index=True)
print(data.shape)
discretizer = MDLP_Discretizer(dataset=data,
                               class_label='e',
                               out_path_data='F:\\JieYuan\\2_WorkProject\\data_log.csv',
                               out_path_bins='F:\\JieYuan\\2_WorkProject\\bin_log.txt' )
```
