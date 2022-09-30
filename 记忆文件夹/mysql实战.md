# 第一章 基础架构



## 1.1 server层

+ 连接器：负责和客户端建立链接，获取权限，维持和管理连接
+ 查询缓存
+ 分析器：词法分析 + 语法分析（分析语法是否正确）
+ 优化器：有多个索引时，决定使用哪个索引；多表关联（join）时，决定表的连接顺序。
+ 执行器：先判断用户是否有权限操作表，然后调用引擎提供的接口



## 1.2 存储引擎

+ InnoDB
+ MyISAM
+ Memory



# 第二章 日志系统





# 第三章 事务隔离



## 3.1 隔离级别

+ 读未提交：一个事务还没提交时，它做的变更就能被别的事务看到
+ 读提交：一个事务提交之后，它做的变更才会被其他事务看到
+ 可重复度：一个事务执行过程中看到的数据，总是跟这个事务在启动时看到的数据是一致的
+ 串行化：同一行记录，“写”会加“写锁”，“读”会加“读锁”。当出现读写锁冲突的时候，后访问的事务必须等前一个事务执行完成，才能继续执行



查看

```mysql
show variables like 'transaction_isolation';
```



## 3.2 隔离级别的实现

每条记录在更新的时候都会同时记录一条回滚操作。记录上的最新值，通过回滚操作，都可以得到前一个状态的值。使用长事务意味着系统里面会存在很老的事务视图，会导致大量占用存储空间。





## 3.3 事务的启动方式

+ 显示启动事务语句

  ```mysql
  begin 或 start transaction。配套的提交语句是 commit，回滚语句是 rollback
  ```

+ set autocommit

  ```mysql
  set autocommit=0，关闭自动提交。事务持续存在直到你主动执行 commit 或 rollback 语句，或者断开连接。建议你总是使用 set autocommit=1, 通过显式语句的方式来启动事务
  ```





# 第四章 索引



## 4.1 索引的常见模型



### 4.1.1 哈希表

适合等值查询，区间查询很慢



### 4.1.2 有序数组

适合等值和区间查询，但是插入记录成本太高



### 4.1.3 搜索树



## 4.2 InnoDB的索引模型



### 4.2.1 索引组织结构

索引类型分为主键索引和非主键索引。主键索引的叶子节点存的是整行数据，非主键索引的叶子节点内容是主键的值。



### 4.2.2 查询过程

1. 基于主键索引的查询可以直接得到整行数据
2. 普通索引查询，先得到主键的值，然后再去主键索引树上搜索一次。
3. 结论：**尽量使用主键查询**



## 4.3 索引维护

插入新记录时，需要维护索引树的有序性。如果主键是自增的，就不会出现数据页分裂的情况，导致性能下降。而且非主键索引树叶子节点上是主键的值，用整数做主键，节约空间。



业务字段做索引的常见

+ 只有一个索引
+ 该索引是唯一索引





## 4.4 索引重建

索引可能因为删除，或者页分裂等原因，导致数据页有空洞，重建索引的过程会创建一个新的索引，把数据按顺序插入，这样页面的利用率高，也就是索引更紧凑、更省空间。

### 4.4.1 重建普通索引

```mysql
alter table T drop index k;
alter table T add index(k);
```





### 4.4.2 重建主键索引

```mysql
#错误的做法
alter table T drop primary key;
alter table T add primary key(id);

#正确的做法
alter table T engine=InnoDB
```





## 4.5 回表



查询语句

```mysql
select * from T where k between 3 and 5
```



表结构

```mysql
create table T (
ID int primary key,
k int NOT NULL DEFAULT 0, 
s varchar(16) NOT NULL DEFAULT '',
index k(k))
engine=InnoDB;

insert into T values(100,1, 'aa'),(200,2,'bb'),(300,3,'cc'),(500,5,'ee'),(600,6,'ff'),(700,7,'gg');
```



执行流程

1. 在 k 索引树上找到 k=3 的记录，取得 ID = 300；
2. 再到 ID 索引树查到 ID=300 对应的 R3；
3. 在 k 索引树取下一个值 k=5，取得 ID=500；
4. 再回到 ID 索引树查到 ID=500 对应的 R4；
5. 在 k 索引树取下一个值 k=6，不满足条件，循环结束。



**查询的过程要先在k索引树查找一次，然后再回到主索引树查找，这个过程称为回表**。





## 4.6 覆盖索引



执行的语句

```mysql
select ID from T where k between 3 and 5
```

不需要回表就能得到结果，称为覆盖索引。**覆盖索引可以减少树的搜索次数，显著提升查询性能，所以使用覆盖索引是一个常用的性能优化手段**





利用覆盖索引优化性能

```mysql

CREATE TABLE `tuser` (
  `id` int(11) NOT NULL,
  `id_card` varchar(32) DEFAULT NULL,
  `name` varchar(32) DEFAULT NULL,
  `age` int(11) DEFAULT NULL,
  `ismale` tinyint(1) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `id_card` (`id_card`),
  KEY `name_age` (`name`,`age`)
) ENGINE=InnoDB
```

建立（身份证，姓名）的联合索引，当根据市民的身份证号查询他的姓名时，就不需要回表了。





## 4.7 最左前缀

当建立了联合索引（name，age）时，使用如下

```mysql
where name like ‘张 %’
```

sql语句时，可以用上索引进行加速，称为最左前缀。



问题：如何安排联合索引内的字段的顺序？

答案：如果通过调整顺序，可以少维护一个索引，那么这个顺序往往就是需要优先考虑采用的



问题：既有联合查询，又有基于 a、b 各自的查询呢？

需要同时维护(a,b) , b 或者 （b,a）,a,看哪个占用的空间大。





## 4.8 索引下推



联合索引：（name，age）



sql语句

```mysql
mysql> select * from tuser where name like '张%' and age=10 and ismale=1;
```

MySQL5.6之后，会进行索引下推优化。索引遍历过程中，对索引中包含的字段先做判断，直接过滤掉不满足条件的记录，减少回表次数。age必须为10 ，才会进行回表。





# 第五章 锁



## 5.1 全局锁

定义： 对整个数据库实例加锁，加锁后整个库处于只读状态。



命令

```mysql
Flush tables with read lock
```



使用场景：全库逻辑备份



缺点:

+ 如果你在主库上备份，那么在备份期间都不能执行更新，业务基本上就得停摆
+ 如果你在从库上备份，那么备份期间从库不能执行主库同步过来的 binlog，会导致主从延迟



不停摆业务情况下备份

mysqldump 使用参数–single-transaction，会在可重复读隔离级别下开启一个事务，进行备份。要求引擎支持这个隔离级别，索引要用InnoDB引擎。



全库只读方案

1. Flush tables with read lock
2. set global readonly=true

建议用第一种方法，第二种方法主要用来判断是否为从库，而且当客户端异常断开后，第二种方法会导致数据库一直处于readonly的状态。





DML：增删改数据

DDL：修改表结构





## 5.2 表级锁



### 5.2.1 表锁

lock tables 会限制其它线程和本线程对表的操作

+ 读锁

  ```mysql
  #表只能读取数据
  lock tables 表名 read;
  ```

+ 写锁

  ```mysql
  #既不能读也不能写
  lock tables 表名 write;
  ```

  



### 5.2.2 元数据锁

不需要显式使用。当对一个表做增删改查操作的时候，加 MDL 读锁；当要对表做结构变更操作的时候，加 MDL 写锁

+ 读锁之间不互斥，因此你可以有多个线程同时对一张表增删改查
+ 读写锁之间、写锁之间是互斥的，用来保证变更表结构操作的安全性。因此，如果有两个线程要同时给一个表加字段，其中一个要等另一个执行完才能开始执行



常见问题：给小表加字段，导致数据库挂掉





安全给小表加字段

1. 在information_schema.innodb_trx中查看当前正在执行的长事务，如果你要做 DDL 变更的表刚好有长事务在执行，要考虑先暂停 DDL，或者 kill 掉这个长事务
2. 在alter table里面设置超时时间。





## 5.3 行锁



### 5.3.1 两阶段锁

在 InnoDB 事务中，行锁是在需要的时候才加上的，但并不是不需要了就立刻释放，而是要等到事务结束时才释放



### 5.3.2 死锁和死锁检测



死锁：当并发系统中不同线程出现循环资源依赖，涉及的线程都在等待别的线程释放资源时，就会导致这几个线程都进入无限等待的状态，称为死锁



解决策略：

1. 直接等待，直到超时。超时时间通过innodb_lock_wait_timeout 设置，超时时间过长，业务无法接受；超时时间太短，会造成误伤。

2. 发起死锁检测。死锁检测会消耗大量CPU。配置参数innodb_deadlock_detect

   ```ini
   [解决死锁检测消耗大量CPU的问题]
   
   A=关闭死锁检测
   
   B=控制客户端的并发
   
   C=更改MySQL的源码
   
   D=一条记录改用几条记录保存
   ```

   

# 第六章 普通索引和唯一索引



## 6.1 查询过程



```mysql
select id from T where k=5
```

普通索引和唯一索引查询性能差距不大。





## 6.2 更新



### 6.2.1 change buffer

当需要更新一个数据页时，如果数据页在内存中就直接更新，而如果这个数据页还没有在内存中的话，在不影响数据一致性的前提下，InnoDB 会将这些更新操作缓存在 change buffer 中，这样就不需要从磁盘中读入这个数据页了。在下次查询需要访问这个数据页的时候，将数据页读入内存，然后执行 change buffer 中与这个页有关的操作。



**change buffer 只有普通索引可以使用，唯一索引不能用**





### 6.2.2 InnoDB插入流程

+ 记录所在目标页在内存中，直接插入

+ 记录所在目标页不在内存中

  ```ini
  [唯一索引]
  将数据页读入内存，判断是否有冲突，插入值，语句执行结束
  
  [普通索引]
  将更新记录在 change buffer，语句执行就结束了
  
  [结论]
  change buffer 因为减少了随机磁盘访问，所以对更新性能的提升是会很明显的
  ```



## 6.3 change buffer 使用场景

对于写多读少的业务来说，页面在写完以后马上被访问到的概率比较小，此时 change buffer 的使用效果最好。这种业务模型常见的就是账单类、日志类的系统





## 6.4 索引选择

尽量选择普通索引。如果所有的更新后面，都马上伴随着对这个记录的查询，那么你应该关闭 change buffer。而在其他情况下，change buffer 都能提升更新性能。





## 6.5 change buffer 和 redo log



假设k1 所在的数据页在内存 (InnoDB buffer pool) 中，k2 所在的数据页不在内存中

```mysql
insert into t(id,k) values(id1,k1),(id2,k2);
```



### 6.5.1 change buffer 更新过程

1. Page 1 在内存中，直接更新内存
2. Page 2 没有在内存中，就在内存的 change buffer 区域，记录下“我要往 Page 2 插入一行”这个信息
3. 将上述两个动作记入 redo log 中





### 6.5.2 change buffer的读取过程

1. 读 Page 1 的时候，直接从内存返回
2. 要读 Page 2 的时候，需要把 Page 2 从磁盘读入内存中，然后应用 change buffer 里面的操作日志，生成一个正确的版本并返回结果





## 6.6 缓存

1. buffer pool：位于存储引擎层

   ```ini
   [缓冲池大小]
   innodb_buffer_pool_size = innodb_buffer_pool_chunk_size * innodb_buffer_pool_instances
   
   [查看参数]
   SELECT @@innodb_buffer_pool_chunk_size;
   
   SELECT @@innodb_buffer_pool_instances;
   
   SELECT @@innodb_buffer_pool_size;
   
   [默认]
   innodb_buffer_pool_instances = 1；
   innodb_buffer_pool_size = 128M;
   innodb_buffer_pool_chunk_size = 128;
   
   [推荐配置]
   # 内存多的话可以配置更大,innodb_buffer_pool_chunk_size不应太大,容易产生竞争
   
   # innodb缓冲池大小
   innodb_buffer_pool_size=4G
    
   # innodb缓冲池块大小
   innodb_buffer_pool_chunk_size=128M
    
   # innodb缓冲池实例数
   innodb_buffer_pool_instances=32
   
   
   [buffer change配置]
   # 占用 buffer pool 的 50%,默认是25
   innodb_change_buffer_max_size = 50;
   ```

   

2. query cache：查询缓存，位于server层，mysql8.0已经删除

3. redo

   ```ini
   [innodb_log_files_in_group]
   desc = redo log 文件的个数,默认为2，推荐设置为4
   
   [innodb_log_file_size]
   desc = 默认48M, 推荐设置为1G
   
   [innodb_log_group_home_dir]
   desc = 文件存放路径
   
   [innodb_log_buffer_size]
   desc = Redo Log缓冲区,默认8M
   
   [innodb_flush_log_at_trx_commit]
   desc = redo log 刷新策略
   
   #每隔1s刷新一次到文件,最极端的情况是丢失1 秒时间的数据变更,速度最快,比设置为1时快10倍
   innodb_flush_log_at_trx_commit = 0
   
   #默认设置,每次事务结束都刷新到磁盘,速度最慢,最安全,数据不会丢失
   innodb_flush_log_at_trx_commit = 1
   
   #每次事务结束，调用文件系统的文件写入操作。而我们的文件系统都是有缓存机制的
   #MySQL Crash 并不会造成数据的丢失，但是OS Crash会导致数据丢失
   #速度比设置为0时稍微慢,但是更加安全
   innodb_flush_log_at_trx_commit = 2
   ```

4. innodb_io_capacity

   ```ini
   [innodb_io_capacity_max]
   desc = 最大刷脏页速度,默认2000,推荐用fio 压测磁盘iops,然后再设置为磁盘最大iops
   
   [innodb_io_capacity]
   desc = 刷脏页速度,默认200,推荐设置为max的50-70%
   
   [测试磁盘iops]
   install = yum install -y fio
   
   # 先设置变量filename,比如filename=bench_buck.tmp
   bench = fio -filename=$filename -direct=1 -iodepth 1 -thread -rw=randrw -ioengine=psync -bs=16k -size=500M -numjobs=10 -runtime=10 -group_reporting -name=mytest
   ```

5. innodb_flush_method

   ```ini
   [可选值]
   fdatasync =  默认
   
   O_DSYNC = 
   
   O_DIRECT = 
   ```

   
