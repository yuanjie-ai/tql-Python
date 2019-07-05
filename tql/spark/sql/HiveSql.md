# Hive快速入门
---
### [Hive内置函数官方][2]
### General Info

For the latest information about Hive, please visit out website at:

http://hive.apache.org/

### Getting Started

- Installation Instructions and a quick tutorial: https://cwiki.apache.org/confluence/display/Hive/GettingStarted

- A longer tutorial that covers more features of HiveQL: https://cwiki.apache.org/confluence/display/Hive/Tutorial

- The HiveQL Language Manual: https://cwiki.apache.org/confluence/display/Hive/LanguageManual

---

DDL：数据库模式定义语言，关键字：create

DML：数据操纵语言，关键字：Insert、delete、update

DCL：数据库控制语言，关键字：grant、remove

DQL：数据库查询语言，关键字：select

---

# 常用
```
LATERAL VIEW udtf(expression) tableAlias AS columnAlias
SELECT table.*, tableAlias.columnAlias FROM table LATERAL VIEW explode('_1') tableAlias AS columnAlias # table->tableAlias虚表

DROP TABLE IF EXISTS fbidm.yuanjie_test;
CREATE TABLE IF NOT EXISTS fbidm.yuanjie_test
TRUNCATE TABLE tablename;
SHOW TABLES LIKE '*name*';
SHOW PARTITIONS table_name;
DESC table_name;
DESC FORMATTED table_name;
SHOW FUNCTIONS;
DESC FUNCTION concat;
SELECT col1[0], col2['b'], col3.c FROM complex; //查看数组、map、结构
FROM temp INSERT overwrite TABLE fbidm.yuanjie_test PARTITION(stat_date='2017-09-14') SELECT id

# 动态分区
set hive.exec.dynamic.partition.mode = nonstrict;
FROM temp INSERT overwrite TABLE fbidm.yuanjie_test PARTITION(stat_date) SELECT *

WITH
t1 AS (),
t2 AS (),
...
select * from t1/t2
```
---

# DDL   
- CREATE TABLE
```
CREATE [TEMPORARY] [EXTERNAL] TABLE [IF NOT EXISTS] [db_name.] table_name
[(col_name data_type [COMMENT col_comment], ...)]
[COMMENT table_comment]
[ROW FORMAT row_format]
[STORED AS file_format]
```
```
CREATE TABLE fbidm.yuanjie_test
(  
  id INT  		COMMENT '标识',  
  name STRING  	COMMENT '姓名',
  height INT 	COMMENT '身高',
  weight INT 	COMMENT '体重',
  age INT 		COMMENT '年龄'
)  
COMMENT '测试分区表'  
PARTITIONED BY(dt STRING COMMENT '时间分区字段')
CLUSTERED BY(id) SORTED BY(name) INTO 32 BUCKETS
ROW FORMAT DELIMITED FIELDS TERMINATED BY ','
STORED AS RCFILE;
```
> RcFile是FaceBook开发的一个集行存储和列存储的优点于一身，压缩比更高，读取列更快，它在MapReduce环境中大规模数据处理中扮演着重要的角色

- 复制一个新表
```
CREATE TABLE empty_table LIKE fbidm.yuanjie_test
```

- ALTER TABLE
    - RENAME TO
    ```
    ALTER TABLE table_name RENAME TO new_table_name
    ALTER TABLE table_name PARTITION partition_spec RENAME TO PARTITION partition_spec;
    ```
    
    - PARTITION
    ```
    ALTER TABLE table_name ADD [IF NOT EXISTS] PARTITION(dt = '2017-08-08')
    ALTER TABLE table_name DROP PARTITION(dt = '2017-08-08')
    ```
    - ADD COLUMNS（默认：字段位置在所有列后面(partition列前)）
    ```
    ALTER TABLE table_name ADD COLUMNS(new_col2 INT)
    ALTER TABLE table_name ADD COLUMNS(new_col2 INT COMMENT 'add columns')
    ALTER TABLE table_name ADD COLUMNS(col_name data_type [COMMENT col_comment], ...)
    ```
    - REPLACE COLUMNS: 对应列覆盖修改
    ```
    ALTER TABLE table_name REPLACE COLUMNS(foo INT COMMENT 'only keep the first column')
    ```
    
    - 修改列的名字、类型、位置、注释
    ```
    ALTER TABLE table_name CHANGE [COLUMN] col_old_name col_new_name column_type [COMMENT col_comment] [FIRST|AFTER column_name]
    ```
    
    - 改变表文件格式与组织
    ```
    ALTER TABLE table_name SET FILEFORMAT file_format
    ALTER TABLE table_name CLUSTERED BY(userid) SORTED BY(viewTime) INTO num_buckets BUCKETS
    ```

```
ALTER TABLE name RENAME TO new_name
ALTER TABLE name ADD COLUMNS (col_spec[, col_spec ...])
ALTER TABLE name DROP [COLUMN] column_name
ALTER TABLE name CHANGE column_name new_name new_type
ALTER TABLE name REPLACE COLUMNS (col_spec[, col_spec ...])
```
---

# DML: INSERT、UPDATE、DELETE
- INSERT
    - 基本模式
    ```
    INSERT OVERWRITE|INTO TABLE tablename1 [PARTITION (partcol1=val1, partcol2=val2 ...)]
    select_statement1 FROM from_statement
    ```
    
    - 多插入模式
    ```
    FROM from_statement
    INSERT OVERWRITE TABLE tablename1 [PARTITION (partcol1=val1, partcol2=val2 ...)]
    select_statement1
    [INSERT OVERWRITE TABLE tablename2 [PARTITION ...] 
    select_statement2] 
    ...
    ```
    
    - 自动分区模式
    ```
    INSERT OVERWRITE TABLE tablename PARTITION (partcol1[=val1],       partcol2[=val2] ...)
    select_statement FROM from_statement
    ```
    
---

# DQL
- [CommonFunctions][1]
> Hive只支持等值连接（equality joins）、外连接（outer joins）和（left semi joins）；
Hive不支持所有非等值的连接，因为非等值连接非常难转化到map/reduce任务；
LEFT，RIGHT和FULL OUTER关键字用于处理join中空记录的情况；
LEFT SEMI JOIN 是 IN/EXISTS 子查询的一种更高效的实现；
join时，每次 map/reduce 任务的逻辑是这样的：reducer会缓存join 序列中除了最后一个表的所有表的记录，再通过最后一个表将结果序列化到文件系统，实践中，应该把最大的那个表写在最后

- join
```
SELECT a.* FROM a JOIN b ON (a.id = b.id);

SELECT a.* FROM a JOIN b ON (a.id = b.id AND a.department = b.department);

SELECT a.val, b.val, c.val FROM a 
JOIN b ON (a.key = b.key1) 
JOIN c ON (c.key = b.key2) //可以join多个表
```
- LEFT SEMI JOIN
```
SELECT a.key, a.value 
  FROM a 
  WHERE a.key in 
   (SELECT b.key 
    FROM B)

SELECT a.key, a.val FROM a LEFT SEMI JOIN b on (a.key = b.key)
```

- UNION ALL
> 用来合并多个select的查询结果，需要保证select中字段须一致

---
  [1]: http://www.aboutyun.com/thread-7316-1-1.html
  [2]: https://cwiki.apache.org/confluence/display/Hive/LanguageManual+UDF
