# [CommonFunctions][0]
## 关系运算
## 数学运算
## 逻辑运算
## 数值运算

---

## [窗口函数](./WindowFunctions.md)
## 日期函数
- 当前日期
```
df.select(F.current_date(), F.current_timestamp()).show(1,False)
+--------------+-----------------------+
|current_date()|current_timestamp()    |
+--------------+-----------------------+
|2017-07-26    |2017-07-26 20:15:24.124|
+--------------+-----------------------+
```
- 当前时间戳  
```
unix_timestamp(timestamp=None, format='yyyy-MM-dd HH:mm:ss')
```
- 当前字段转时间戳
```
unix_timestamp(timestamp='字段', format='yyyy-MM-dd HH:mm:ss')
```
- 时间戳转日期字符串（与上反向）
```
from_unixtime(timestamp='字段', format='yyyy-MM-dd HH:mm:ss')
```

- 日期提取: Extract the year/month/week/day/hour/minute/second of a given date as integer
    - year(col)
    - month(col)
    - dayofyear(col)
    - dayofmonth(col)
    - dayofweek(col)
    - weekofyear(col)
    - hour(col)
    - minute(col)
    - second(col)
- 日期运算
    - last_day(date): 当月最后一天
    - next_day(startdate, dayOfWeek)
    ```
    # dayOfWeek = "Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"
    spark.createDataFrame([('2017-07-26',)]).select(next_day('_1', 'Sun')).show()
    +-----------------+
    |next_day(_1, Sun)|
    +-----------------+
    |       2017-07-30|
    +-----------------+
    ```
    - date_format(date, format)
    ```
    spark.createDataFrame([('2015-04-08',)]).select(date_format('_1', 'MM/dd/yyy')).show()
    +--------------------------+
    |date_format(_1, MM/dd/yyy)|
    +--------------------------+
    |                04/08/2015|
    +--------------------------+
    ```
    
    - date_add(start, days)
    - date_sub(start, days)
    - add_months(start, months)
    - months_between(date1, date2)
    - datediff(end, start)
    - to_date(col)

## 条件函数
- if(Test Condition, True Value, False Value )
    - R: ifelse
    - python: np.where

- COALESCE(T v1, T v2, …): 返回第一个非空的列
```
df = spark.createDataFrame([(None, None), (1, None), (None, 2)], ("a", "b"))
df.select('*', F.coalesce(df["a"], df["b"])).show()
+----+----+--------------+
|   a|   b|coalesce(a, b)|
+----+----+--------------+
|null|null|          null|
|   1|null|             1|
|null|   2|             2|
+----+----+--------------+
```
```
df.select('*', F.coalesce(df["a"], F.lit(0.0))).show()
+----+----+----------------+
|   a|   b|coalesce(a, 0.0)|
+----+----+----------------+
|null|null|             0.0|
|   1|null|             1.0|
|null|   2|             0.0|
+----+----+----------------+
```
- CASE: spark when(condition, T value).otherwise(F value)
    - 简单Case函数
    ```
    CASE a WHEN b THEN c ELSE c END
    
    CASE sex
    WHEN '1' THEN '男'
    WHEN '2' THEN '女'
    ELSE '其他' END
    ```
    - Case搜索函数
    
    ```
    CASE WHEN a THEN b ELSE c END
    
    CASE WHEN sex = '1' THEN '男' 
    WHEN sex = '2' THEN '女' 
    ELSE '其他' END 
    ```
    
---

## 字符串函数
- length(col)
- reverse(col)
- concat(*cols)
- concat_ws(sep, *cols)
- split(str, pattern): 分割字符串
- substring(str, pos, len): 字符串截取
- upper(col): 字符串转大写
- lower(col): 字符串转小写
- trim(col): 去空格
    - ltrim(col): 左边去空格
    - rtrim(col):右边去空格
- regexp_extract(str, pattern, idx): 正则表达式解析函数
- regexp_replace(str, pattern, replacement): 正则表达式替换函数
- parse_url(url, partToExtract[, key])
- parse_url_tuple(url, p1, p2 ...)
> partToExtract选项包含[HOST,PATH,QUERY,REF,PROTOCOL,FILE,AUTHORITY,USERINFO]

```
df.selectExpr("parse_url('http://facebook.com/path/p1.php?query=1', 'HOST')").show()
+--------------------------------------------------------+
|parse_url(http://facebook.com/path/p1.php?query=1, HOST)|
+--------------------------------------------------------+
|                                            facebook.com|
|                                            facebook.com|
|                                            facebook.com|
+--------------------------------------------------------+
```

- get_json_object(col, path): json解析函数('$.f1'取键)
```
data = [("1", '''{"f1": "value1", "f2": "value2"}'''), ("2", '''{"f1": "value12"}''')]
df = spark.createDataFrame(data, ("key", "jstring"))
df.select(df.key, F.get_json_object(df.jstring, '$.f1').alias("c0"), \
                  F.get_json_object(df.jstring, '$.f2').alias("c1") ).show()
+---+-------+------+
|key|     c0|    c1|
+---+-------+------+
|  1| value1|value2|
|  2|value12|  null|
+---+-------+------+
```

- space(n): 返回n个空格字符串
- repeat(col, n): 重复字符串n次
- ascii(col): 首字符ascii 计算字符串列的第一个字符的数值
- lpad(col, len, pad)
- rpad(col, len, pad)
```
spark.createDataFrame([('abcd',)]).select(lpad('_1', 8, '-'), rpad('_1', 8, '-')).show()
+--------------+--------------+
|lpad(_1, 8, -)|rpad(_1, 8, -)|
+--------------+--------------+
|      ----abcd|      abcd----|
+--------------+--------------+
```
- find_in_set(str,str_array):
>  返回str_array中str的第一次出现，其中str_array是以逗号分隔的字符串。如果任一参数为空，则返回null。 如果第一个参数有逗号，则返回0。

```
df.selectExpr("find_in_set('a', 'b,a')").show()
+-------------------+
|find_in_set(a, b,a)|
+-------------------+
|                  2|
+-------------------+
```
---

## 集合函数
- histogram_numeric: 直方图
```
spark.range(10).selectExpr("histogram_numeric(id, 5)").show(1,False)
+-------------------------------------------------------+
|histogram_numeric( id, 5)                              |
+-------------------------------------------------------+
|[[0.5,2.0], [2.0,1.0], [3.5,2.0], [5.5,2.0], [8.0,3.0]]|
+-------------------------------------------------------+
```
- count
- sum
- avg
- mean
- max
- min
- percentile(col, p): 中位数
- percentile_approx(col, p [, B])： 近似中位数
- var_pop(col): 组内总体方差
- var_samp(col): 组内总体无偏(unbiased)方差
- stddev_pop(col): 总体标准偏差
- stddev_samp(col): 样本标准偏差
---

## 复合类型构建操作
- Map类型构建: map
- Struct类型构建: struct
- array类型构建: array
---

## 复杂类型访问操作
- array类型访问: A[n]
- map类型访问: M[key]
- struct类型访问: S.x
---

## 复杂类型长度统计函数
- Map类型长度函数: size(Map<K.V>)
- array类型长度函数: size(Array<T>)
- 类型转换函数: cast(expr as <type>)

---
[0]: https://cwiki.apache.org/confluence/display/Hive/Tutorial#Tutorial-BuiltInFunctions

