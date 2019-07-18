# 查询优化设置
```
//job name
set mapreduce.job.name = JieYuan_job;
set hive.exec.dynamic.partition.mode=nonstrict;
set hive.exec.mode.local.auto=true; //当一个job满足如下条件会使用本地模式
set hive.exec.parallel=true; //开启并行模式
set hive.exec.parallel.thread.number=16; //最大64
set hive.merge.mapfiles=true; //map任务输出合并
set hive.merge.mapredfiles=true; //mr任务输出合并
set mapred.compress.map.output=true; //减少IO开启中间结果压缩
set mapred.compress.output.compression.codec=com.hadoop.compression.lzo.LzoCodec; //设置压缩算法
//join
set hive.auto.convert.join = true;
set mapred.reduce.tasks = -1; //代表自动根据作业的情况来设置reduce的值
set hive.optimize.bucketmapjoin = true;
//数据倾斜
set hive.optimize.skewjoin = true;
set hive.groupby.skewindata = true;
```
---
# 常用优化参数
- hive.exec.max.created.files
    - 说明：所有hive运行的map与reduce任务可以产生的文件的和
    - 默认值:100000 
- hive.exec.dynamic.partition
    - 说明：是否为自动分区
    - 默认值：false
- hive.mapred.reduce.tasks.speculative.execution
    - 说明：是否打开推测执行
    - 默认值：true
- hive.input.format
    - 说明：Hive默认的input format
    - 默认值： org.apache.hadoop.hive.ql.io.CombineHiveInputFormat
    - 如果有问题可以使用org.apache.hadoop.hive.ql.io.HiveInputFormat
- hive.exec.counters.pull.interval
    - 说明：Hive与JobTracker拉取counter信息的时间
    - 默认值：1000ms 
- hive.script.recordreader
    - 说明：使用脚本时默认的读取类
    - 默认值： org.apache.hadoop.hive.ql.exec.TextRecordReader
- hive.script.recordwriter
    - 说明：使用脚本时默认的数据写入类
    - 默认值： org.apache.hadoop.hive.ql.exec.TextRecordWriter
- hive.mapjoin.check.memory.rows
    - 说明： 内存里可以存储数据的行数
    - 默认值： 100000
- hive.mapjoin.smalltable.filesize
    - 说明：输入小表的文件大小的阀值，如果小于该值，就采用普通的join
    - 默认值： 25000000
- hive.auto.convert.join
    - 说明：是不是依据输入文件的大小，将Join转成普通的Map Join
    - 默认值： false
- hive.mapjoin.followby.gby.localtask.max.memory.usage
    - 说明：map join做group by 操作时，可以使用多大的内存来存储数据，如果数据太大，则不会保存在内存里
    - 默认值：0.55
- hive.mapjoin.localtask.max.memory.usage
    - 说明：本地任务可以使用内存的百分比
    - 默认值： 0.90
- hive.heartbeat.interval
    - 说明：在进行MapJoin与过滤操作时，发送心跳的时间
    - 默认值1000
- hive.merge.size.per.task
    - 说明： 合并后文件的大小
    - 默认值： 256000000
- hive.mergejob.maponly
    - 说明： 在只有Map任务的时候 合并输出结果
    - 默认值： true
- hive.merge.mapredfiles
    - 默认值： 在作业结束的时候是否合并小文件
    - 说明： false
- hive.merge.mapfiles
    - 说明：Map-Only Job是否合并小文件
    - 默认值：true
- hive.hwi.listen.host
    - 说明：Hive UI 默认的host
    - 默认值：0.0.0.0
- hive.hwi.listen.port
    - 说明：Ui监听端口
    - 默认值：9999
- hive.exec.parallel.thread.number
    - 说明：hive可以并行处理Job的线程数
    - 默认值：8
- hive.exec.parallel
    - 说明：是否并行提交任务
    - 默认值：false
- hive.exec.compress.output
    - 说明：输出使用压缩
    - 默认值： false
- hive.mapred.mode
    - 说明： MapReduce的操作的限制模式，操作的运行在该模式下没有什么限制
    - 默认值： nonstrict
- hive.join.cache.size
    - 说明： join操作时，可以存在内存里的条数
    - 默认值： 25000
- hive.mapjoin.cache.numrows
    - 说明： mapjoin 存在内存里的数据量
    - 默认值：25000
- hive.join.emit.interval
    - 说明： 有连接时Hive在输出前，缓存的时间
    - 默认值： 1000
- hive.optimize.groupby
    - 说明：在做分组统计时，是否使用bucket table
    - 默认值： true
- hive.fileformat.check
    - 说明：是否检测文件输入格式
    - 默认值：true
- hive.metastore.client.connect.retry.delay
    - 说明： client 连接失败时,retry的时间间隔
    - 默认值：1秒
- hive.metastore.client.socket.timeout
    - 说明:  Client socket 的超时时间
    - 默认值：20秒
- mapred.reduce.tasks
    - 默认值：-1(代表自动根据作业的情况来设置reduce的值)
    - 说明：每个任务reduce的默认值
- hive.exec.reducers.bytes.per.reducer
    - 默认值： 1000000000 （1G）
    - 说明：每个reduce的接受的数据量,如果送到reduce的数据为10G,那么将生成10个reduce任务
- hive.exec.reducers.max
    - 默认值：999
    - 说明： reduce的最大个数      
- hive.exec.reducers.max
    - 默认值：999
    - 说明： reduce的最大个数
- hive.metastore.warehouse.dir
    - 默认值：/user/hive/warehouse
    - 说明： 默认的数据库存放位置
- hive.default.fileformat
    - 默认值：TextFile
    - 说明： 默认的fileformat
- hive.map.aggr
    - 默认值：true
    - 说明： Map端聚合，相当于combiner
- hive.exec.max.dynamic.partitions.pernode
    - 默认值：100
    - 说明：每个任务节点可以产生的最大的分区数
- hive.exec.max.dynamic.partitions
    - 默认值：1000
    - 说明： 默认的可以创建的分区数
- hive.metastore.server.max.threads
    - 默认值：100000
    - 说明： metastore默认的最大的处理线程数
- hive.metastore.server.min.threads
    - 默认值：200
    - 说明： metastore默认的最小的处理线程数
    
- set mapreduce.jobtracker.split.metainfo.maxsize = -1
   - 如果输入文件过多，会造成split源文件超过默认值，需要调整该参数。

# 参考
- [Hive常用优化参数][1]


  [1]: http://blog.csdn.net/q412774506/article/details/46998713

