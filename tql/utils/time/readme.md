## [日期/时间特征][1]
- 基础特征
```python
import pandas as pd
t = pd.Timestamp(pd.datetime.today())
t.year
t.quarter
t.month # t.month_name
t.day
t.hour
t.minute
t.second

t.week
t.weekday() # t.weekday_name
t.weekofyear
```

- 时间窗口统计特征
    - 将时间分成若干个窗口，在每个窗口中进行特征提取
- 差分统计特征
    - 在一个周期内，同个时刻数值的增长率，或其他对比方式 
- 转换特征
    - 取对数，做差，做除等等

- 分解特征
    - 季节性
    - 周期性
    - 趋势性
    - 残差性

- LSTM


---
[1]: https://jvn.io/Jie-Yuan/c28a48c1c93d4ca692a43f750af502d6