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



## 2.1 binary log

redo log 是 InnoDB 引擎特有的日志，而 Server 层也有自己的日志，称为 binlog

### 2.1.1 常用命令

```mysql
#查看日志开启状态 
SHOW VARIABLES LIKE 'log_bin';

+---------------+-------+
| Variable_name | Value |
+---------------+-------+
| log_bin       | OFF   |
+---------------+-------+

#查看当前正在写入的binlog文件
show master status \G;


#查看指定binlog内容
show binlog events in 'mysql-bin.000001';


#查看所有binlog日志列表
show master logs;


#刷新log日志，立刻产生一个新编号的binlog日志文件，跟重启一个效果 
flush logs;


#清空所有binlog日志 
reset master;

#使用binlog恢复数据[未测试]
/usr/bin/mysqlbinlog  –start-datetime=’2011-7-7 18:0:0′–stop-datetime=’2011-7-7 20:07:13′ data/mysql-bin.000008 |mysql -u root
```



### 2.1.2 配置

```ini
[mysqld]
#设置日志三种格式：statement、row、mixed 。
binlog_format = statement
#设置日志路径，注意路经需要mysql用户有权限写
log-bin = /var/lib/mysql/mysql-bin
#设置binlog清理时间
expire_logs_days = 7
#binlog每个日志文件大小
max_binlog_size = 100m
#binlog缓存大小
binlog_cache_size = 4m
#最大binlog缓存大小
max_binlog_cache_size = 512m
server-id=1

#配置binary log 同步到磁盘的频率,为0时性能最好,1性能最差,也可以配置为100或者1000
sync_binlog = 0

# sync_binlog=0，当事务提交之后，MySQL不做fsync之类的磁盘同步指令刷新binlog_cache中的信息到磁盘，而让Filesystem自行决定什么时候来做同步，或者cache满了之后才同步到磁盘。这个是性能最好的。

# sync_binlog=1，当每进行1次事务提交之后，MySQL将进行一次fsync之类的磁盘同步指令来将binlog_cache中的数据强制写入磁盘,这是默认值,性能最差

# sync_binlog=n，当每进行n次事务提交之后，MySQL将进行一次fsync之类的磁盘同步指令来将binlog_cache中的数据强制写入磁盘。[推荐配置为1000]
```



简单配置

```shell
#第一种方式:
#开启binlog日志
log_bin=ON
#binlog日志的基本文件名
log_bin_basename=/var/lib/mysql/mysql-bin
#binlog文件的索引文件，管理所有binlog文件
log_bin_index=/var/lib/mysql/mysql-bin.index
#配置serverid
server-id=1

#第二种方式:
#此一行等同于上面log_bin三行
log-bin=/var/lib/mysql/mysql-bin
#配置serverid
server-id=1
```





### 2.1.3 三种模式对比

1. STATEMENT

   ```
   基于SQL语句的复制(statement-based replication, SBR)，每一条会修改数据的sql语句会记录到binlog中
   ```

2. ROW

   ```
   基于行的复制(row-based replication, RBR)格式：不记录每一条SQL语句的上下文信息，仅需记录哪条数据被修改了，修改成了什么样子了
   ```

3. MIXED

   ```
   混合模式复制(mixed-based replication, MBR)：以上两种模式的混合使用
   ```




### 2.1.4 对比

1. redo log 是 InnoDB 引擎特有的；binlog 是 MySQL 的 Server 层实现的，所有引擎都可以使用
2. redo log 是物理日志，记录的是“在某个数据页上做了什么修改”；binlog 是逻辑日志，记录的是这个语句的原始逻辑，比如“给 ID=2 这一行的 c 字段加 1 ”
3. redo log 是循环写的，空间固定会用完；binlog 是可以追加写入的。“追加写”是指 binlog 文件写到一定大小后会切换到下一个，并不会覆盖以前的日志



### 2.1.5 更新语句执行流程
```SQL
update T set c=c+1 where ID=2;
```

1. 执行器先找引擎取 ID=2 这一行。ID 是主键，引擎直接用树搜索找到这一行。如果 ID=2 这一行所在的数据页本来就在内存中，就直接返回给执行器；否则，需要先从磁盘读入内存，然后再返回
2. 执行器拿到引擎给的行数据，把这个值加上 1，比如原来是 N，现在就是 N+1，得到新的一行数据，再调用引擎接口写入这行新数据
3. 引擎将这行新数据更新到内存中，同时将这个更新操作记录到 redo log 里面，此时 redo log 处于 prepare 状态。然后告知执行器执行完成了，随时可以提交事务
4. 执行器生成这个操作的 binlog，并把 binlog 写入磁盘
5. 执行器调用引擎的提交事务接口，引擎把刚刚写入的 redo log 改成提交（commit）状态，更新完成







## 2.2 redo log

原理：当有一条记录需要更新的时候，InnoDB 引擎就会先把记录写到 redo log（粉板）里面，并更新内存，这个时候更新就算完成了。同时，InnoDB 引擎会在适当的时候，将这个操作记录更新到磁盘里面，而这个更新往往是在系统比较空闲的时候做，这就像打烊以后掌柜做的事。



### 2.2.1 配置

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
#速度比设置为0时稍微慢,但是更加安全[推荐的配置]
innodb_flush_log_at_trx_commit = 2
```





## 2.3 两阶段提交

定义：将 redo log 的写入拆成了两个步骤：prepare 和 commit，这就是"两阶段提交"。



### 2.3.1 数据恢复过程

1. 首先，找到最近的一次全量备份，如果你运气好，可能就是昨天晚上的一个备份，从这个备份恢复到临时库
2. 然后，从备份的时间点开始，将备份的 binlog 依次取出来，重放到中午误删表之前的那个时刻



结论：如果不使用“两阶段提交”，那么数据库的状态就有可能和用它的日志恢复出来的库的状态不一致



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
  begin 或 start transaction 或 start transaction with consistent snapshot;。配套的提交语句是 commit，回滚语句是 rollback
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

加锁语句

```ini
[共享锁]
sql = select * from test lock in share mode;

[排他锁]
sql-1 = select * from test for update;
sql-2 = insert into test values(…);
sql-3 = update test set …;
sql-4 = delete from test …;

[快照读]
sql  = select * from test;
desc = InnoDB不加任何锁

[当前读]
sql-1 = select * from test lock in share mode;

;使用场景:假设有A、B两个用户同时各购买一件 id=1 的商品，使用可重复读,用户A获取到的库存量为 1000，用户B获取到的库存量也为 1000，用户A完成购买后修改该商品的库存量为 999，用户B完成购买后修改该商品的库存量为 999，此时库存量数据产生了不一致
sql-2 = select * from test for update;
desc  = 当前读会加锁
```





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
   ;问题:如果一台服务器只跑MySQL,buffer pool的大小设置为主机的百分之多少合适
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
   
   [innodb_flush_neighbors]
   desc = 刷一个脏页的时候，如果这个数据页旁边的数据页刚好是脏页，就会把这个“邻居”也带着一起刷掉；而且这个把“邻居”拖下水的逻辑还可以继续蔓延，也就是对于每个邻居数据页，如果跟它相邻的数据页也还是脏页的话，也会被放到一起刷
   默认值 = 1(开启),建议设置为0
   
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



# 第七章 MySQL选错索引



慢查询日志

```ini
[slow_query_log]
desc = 慢查询开启状态

[slow_query_log_file]
desc = 慢查询日志存放位置

[long_query_time]
desc = 超过多少秒才记录,设置为0会记录全部

[查看值cmd]
SHOW VARIABLES LIKE 'slow_query_log';
SHOW VARIABLES LIKE 'long_query_time';
SHOW VARIABLES LIKE 'slow_query_log_file';

[临时开启慢查询日志]
set global slow_query_log=on;

[临时设置时间]
set global long_query_time = 0;
```





分析sql语句执行过程[选择哪些索引，扫描了多少行]

```mysql
explain select * from t where a between 10000 and 20000
```



## 7.1 优化器的逻辑

优化器会根据扫描行数，是否使用临时表，是否排序来综合判断选择哪个索引。



### 7.1.1 如何判断扫描行数

通过索引基数判断。



### 7.1.2 查看索引基数

```mysql
#Cardinality 那一列就是基数
show index from t;
```



### 7.1.3 如何得到索引基数

选择 N 个数据页，统计这些页面上的不同值，得到一个平均值，然后乘以这个索引的页面数，就得到了这个索引的基数。当变更的数据行数超过 1/M 的时候，会自动触发重新做一次索引统计



### 7.1.4 修正索引统计信息

```mysql
analyze table t
```





## 7.2 索引选择异常处理



### 7.2.1 force index

```mysql
#强制选择索引a
select * from t force index(a) where (a between 1 and 1000) and (b between 50000 and 100000) order by b limit 1;
```





### 7.2.2 删掉多余的索引

在这个例子中把索引b删掉







# 第八章 给字符串加索引



## 8.1 完整索引

比较占用空间，索引选取的越长，占用的磁盘空间就越大，相同的数据页能放下的索引值就越少，搜索的效率也就会越低。扫描行数少。



## 8.2 前缀索引

+ 节约空间

+ 增加了扫描次数

+ 如何确定前缀位数

  ```mysql
  #算出这个列上有多少个不同值
  select count(distinct email) as L from SUser;
  
  #选择不同前缀查看这个值
  select 
    count(distinct left(email,4)）as L4,
    count(distinct left(email,5)）as L5,
    count(distinct left(email,6)）as L6,
    count(distinct left(email,7)）as L7,
  from SUser;
          
  #在返回的 L4~L7 中，找出不小于 L * 95% 的值
  ```

  

## 8.3 倒序存储





## 8.4 使用hash

在表上再创建一个整数字段，来保存身份证的hash值，同时在这个字段上创建索引，推荐使用crc32算法。





# 第九章 MySQL抖动

问题：一条 SQL 语句，正常执行的时候特别快，但是有时也不知道怎么回事，它就会变得特别慢，并且这样的场景很难复现，它不只随机，而且持续时间还很短





## 9.1 更新语句流程



### 9.1.1 流程

1. 更新内存
2. 写redo log
3. 返回给客户端



### 9.1.2 脏页

内存数据页跟磁盘数据页内容不一致的时候，我们称这个内存页为“脏页”



### 9.1.3 干净页

内存数据写入到磁盘后，内存和磁盘上的数据页的内容就一致了，称为“干净页”





## 9.2 引发flush的情况

1. InnoDB 的 redo log 写满了。这时候系统会停止所有更新操作，把 checkpoint 往前推进，redo log 留出空间可以继续写
2. 系统内存不足。当需要新的内存页，而内存不够用的时候，就要淘汰一些数据页，空出内存给别的数据页使用。如果淘汰的是“脏页”，就要先将脏页写到磁盘。
3. MySQL 认为系统“空闲”的时候
4. MySQL 正常关闭



## 9.3 上面四种场景对性能影响

1. 更新全部堵住，写性能跌为 0，这种情况对敏感业务来说，是不能接受的
2. 一个查询要淘汰的脏页个数太多，会导致查询的响应时间明显变长



## 9.4 刷脏页控制策略

1. InnoDB 你的磁盘能力。这个值我建议你设置成磁盘的 IOPS

   ```ini
   [innodb_io_capacity] 
   desc = InnoDB后台任务每秒可用的I/O操作数（IOPS），例如用于从buffer pool中刷新脏页和从change buffer中合并数据,建议为innodb_io_capacity_max 的 50 -75%
   
   ;默认200,单盘SATA的配置,如果是固态硬盘可以配置到5000或者压测后配置
   default value = 200
   
   [innodb_io_capacity_max]
   desc = InnoDB后台任务每秒可用的最大I/O操作数（IOPS）
   ```

   磁盘iops压测工具

   ```shell
   fio -filename=$filename -direct=1 -iodepth 1 -thread -rw=randrw -ioengine=psync -bs=16k -size=500M -numjobs=10 -runtime=10 -group_reporting -name=mytest 
   ```

   

2. 监控脏页比例

   ```sql
   
   mysql> select VARIABLE_VALUE into @a from global_status where VARIABLE_NAME = 'Innodb_buffer_pool_pages_dirty';
   select VARIABLE_VALUE into @b from global_status where VARIABLE_NAME = 'Innodb_buffer_pool_pages_total';
   select @a/@b;
   ```

3. 禁止刷邻居脏页

   ```shell
   innodb_flush_neighbors = 0
   ```

   



## 9.5 结论

SQL语句变慢主要是以下两个原因

1. redo log写满导致刷脏页（配置redo log的大小）
2. 查询时系统内存不足，需要新的内存页时，要淘汰一些数据页，淘汰的数据页正好是脏页（增加buffer pool）



# 第十章 删除表数据

一个数据库用一个文件夹保存。一个表用两个文件来保存，.frm是表结构，.ibd是数据。

相关配置项

```ini
[innodb_file_per_table]
desc = 表数据既可以存在共享表空间里，也可以是单独的文件,这个行为由参数innodb_file_per_table决定

value = ON,每个 InnoDB 表数据存储在一个以 .ibd 为后缀的文件中

value = OFF,表的数据放在系统共享表空间，也就是跟数据字典放在一起

;;从 MySQL 5.6.6 版本开始，它的默认值就是 ON 了,建议不管哪个版本都设置为ON
```





## 10.1 数据删除流程

delete 命令其实只是把记录的位置，或者数据页标记为了“可复用”，但磁盘文件的大小是不会变的。



引申：经过大量增加，删除，修改的表，会存在很多空洞，如果可以把这些空洞去掉，就能达到收缩表空间的目的。





## 10.2 重建表

作用：去除空洞



命令

```mysql
alter table A engine=InnoDB
```





## 10.3 重建表的常见方式

+ 方式一

  ```mysql
  #推荐的方式
  alter table t engine = InnoDB
  ```

+ 方式二

  ```mysql
  #这不是重建表，只是对表的索引信息做重新统计，没有修改数据
  analyze table t
  ```

+ 方式三

  ```mysql
  #等于recreate+analyze
  optimize table t
  ```

  

# 第十一章 计算表的行数



## 11.1 count(*)的实现方式

+ MyISAM 引擎把一个表的总行数存在了磁盘上，因此执行 count(*) 的时候会直接返回这个数，效率很高
+  InnoDB 引擎就麻烦了，它执行 count(*) 的时候，需要把数据一行一行地从引擎里面读出来，然后累积计数





## 11.2 InnoDB不存count(*)的原因

InnoDB 的事务设计有关系，可重复读是它默认的隔离级别，在代码上就是通过多版本并发控制，也就是 MVCC 来实现的。每一行记录都要判断自己是否对这个会话可见，因此对于 count(*) 请求来说，InnoDB 只好把数据一行一行地读出依次判断，可见的行才能够用于计算“基于这个查询”的表的总行数





## 11.3 自己计数



### 11.3.1 使用缓存系统计数

+ 可能会丢失更新
+ 缓存系统不支持事务操作，多个回话时，会导致计数逻辑错误。





### 11.3.2 数据库保存计数

利用MySQL的事务特性，可以确保数据不丢失，并且计数逻辑正确





## 11.4 不同count对比

count(字段)<count(主键 id)<count(1)≈count(\*)，所以我建议你，尽量使用 count(\*)





# 第十二章 Order by排序

表结构

```mysql
CREATE TABLE `t` (
  `id` int(11) NOT NULL,
  `city` varchar(16) NOT NULL,
  `name` varchar(16) NOT NULL,
  `age` int(11) NOT NULL,
  `addr` varchar(128) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `city` (`city`)
) ENGINE=InnoDB;
```



查询语句

```mysql
select city,name,age from t where city='杭州' order by name limit 1000  ;
```





## 12.1 全字段排序



### 12.1.1 排序过程

1. 初始化 sort_buffer，确定放入 name、city、age 这三个字段；
2. 从索引 city 找到第一个满足 city='杭州’条件的主键 id，也就是图中的 ID_X；
3. 到主键 id 索引取出整行，取 name、city、age 三个字段的值，存入 sort_buffer 中；
4. 从索引 city 取下一个记录的主键 id；
5. 重复步骤 3、4 直到 city 的值不满足查询条件为止，对应的主键 id 也就是图中的 ID_Y；
6. 对 sort_buffer 中的数据按照字段 name 做快速排序；
7. 按照排序结果取前 1000 行返回给客户端。



### 12.1.2 确定是否使用临时表

```mysql

/* 打开optimizer_trace，只对本线程有效 */
SET optimizer_trace='enabled=on'; 

/* @a保存Innodb_rows_read的初始值 */
select VARIABLE_VALUE into @a from  performance_schema.session_status where variable_name = 'Innodb_rows_read';

/* 执行语句 */
select city, name,age from t where city='杭州' order by name limit 1000; 

/* 查看 OPTIMIZER_TRACE 输出 */
SELECT * FROM `information_schema`.`OPTIMIZER_TRACE`\G

/* @b保存Innodb_rows_read的当前值 */
select VARIABLE_VALUE into @b from performance_schema.session_status where variable_name = 'Innodb_rows_read';

/* 计算Innodb_rows_read差值 */
select @b-@a;
```



结果：number_of_tmp_files表示使用的临时文件个数。如果 sort_buffer_size 超过了需要排序的数据量的大小，number_of_tmp_files 就是 0，表示排序可以直接在内存中完成。否则就需要放在临时文件中排序。可以在配置文件里面配置sort_buffer_size 的大小

```json
            "filesort_execution": [
            ],
            "filesort_summary": {
              "rows": 16781,
              "examined_rows": 16781,
              "number_of_tmp_files": 35,
              "sort_buffer_size": 32760,
              "sort_mode": "<sort_key, packed_additional_fields>"
            }

```





## 12.2 rowid排序

MySQL 认为排序的单行长度太大，就只将要排序的列和主键id放入sort_buffer进行排序。



### 12.2.1 设置

```mysql
/*单行的长度超过这个值，MySQL 就认为单行太大，要换一个算法*/
SET max_length_for_sort_data = 16;
```



### 12.2.2 排序过程

1. 初始化 sort_buffer，确定放入两个字段，即 name 和 id；
2. 从索引 city 找到第一个满足 city='杭州’条件的主键 id，也就是图中的 ID_X；
3. 到主键 id 索引取出整行，取 name、id 这两个字段，存入 sort_buffer 中；
4. 从索引 city 取下一个记录的主键 id；
5. 重复步骤 3、4 直到不满足 city='杭州’条件为止，也就是图中的 ID_Y；
6. 对 sort_buffer 中的数据按照字段 name 进行排序；
7. 遍历排序结果，取前 1000 行，并按照 id 的值回到原表中取出 city、name 和 age 三个字段返回给客户端。



## 12.3 两种排序对比

rowid 排序会要求回表多造成磁盘读，因此不会被优先选择，所以业务有很多order by 操作时，可以把sort_buffer_size 设置得大一些。



## 12.4 Order by语句优化





### 12.4.1 创建city和 name的联合索引

```mysql
alter table t add index city_user(city, name);
```



查询流程

1. 从索引 (city,name) 找到第一个满足 city='杭州’条件的主键 id；
2. 到主键 id 索引取出整行，取 name、city、age 三个字段的值，作为结果集的一部分直接返回；
3. 从索引 (city,name) 取下一个记录主键 id；
4. 重复步骤 2、3，直到查到第 1000 条记录，或者是不满足 city='杭州’条件时循环结束。



### 12.4.2 创建city、name和age的联合索引

```mysql
alter table t add index city_user_age(city, name, age);
```

流程和上面类似，但是不需要回表，速度更快





# 第十三章 随机显示单词



建表

```sql
CREATE TABLE `words` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `word` varchar(64) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

delimiter ;;
create procedure idata()
begin
  declare i int;
  set i=0;
  while i<10000 do
    insert into words(word) values(concat(char(97+(i div 1000)), char(97+(i % 1000 div 100)), char(97+(i % 100 div 10)), char(97+(i % 10))));
    set i=i+1;
  end while;
end;;
delimiter ;

call idata();
```



## 13.1 内存临时表



### 13.1.1 查询语句

```sql
select word from words order by rand() limit 3;
```



### 13.1.2 查看语句执行情况

```sql
explain select word from words order by rand() limit 3;

+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+---------------------------------+
| id | select_type | table | partitions | type | possible_keys | key  | key_len | ref  | rows | filtered | Extra                           |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+---------------------------------+
|  1 | SIMPLE      | words | NULL       | ALL  | NULL          | NULL | NULL    | NULL | 9980 |   100.00 | Using temporary; Using filesort |
+----+-------------+-------+------------+------+---------------+------+---------+------+------+----------+---------------------------------+


#Using temporary，表示的是需要使用临时表；Using filesort，表示的是需要执行排序操作。
```



### 13.1.3 排序方式

内存表使用rowid排序，回表过程只是简单地根据数据行的位置，直接访问内存得到数据，根本不会导致多访问磁盘。





### 13.1.4 执行流程

1. 创建一个临时表。这个临时表使用的是 memory 引擎，表里有两个字段，第一个字段是 double 类型，为了后面描述方便，记为字段 R，第二个字段是 varchar(64) 类型，记为字段 W。并且，这个表没有建索引
2. 从 words 表中，按主键顺序取出所有的 word 值。对于每一个 word 值，调用 rand() 函数生成一个大于 0 小于 1 的随机小数，并把这个随机小数和 word 分别存入临时表的 R 和 W 字段中，到此，扫描行数是 10000。
3. 现在临时表有 10000 行数据了，接下来你要在这个没有索引的内存临时表上，按照字段 R 排序。
4. 初始化 sort_buffer。sort_buffer 中有两个字段，一个是 double 类型，另一个是整型。
5. 从内存临时表中一行一行地取出 R 值和位置信息（我后面会和你解释这里为什么是“位置信息”），分别存入 sort_buffer 中的两个字段里。这个过程要对内存临时表做全表扫描，此时扫描行数增加 10000，变成了 20000。
6. 在 sort_buffer 中根据 R 的值进行排序。注意，这个过程没有涉及到表操作，所以不会增加扫描行数。
7. 排序完成后，取出前三个结果的位置信息，依次到内存临时表中取出 word 值，返回给客户端。这个过程中，访问了表的三行数据，总扫描行数变成了 20003。



## 13.2 磁盘临时表



问题：是不是所有的临时表都是内存表呢

答案：tmp_table_size 这个配置限制了内存临时表的大小，默认值是 16M。如果临时表大小超过了 tmp_table_size，那么内存临时表就会转成磁盘临时表



复现使用磁盘临时表

```sql

set tmp_table_size=1024;
set sort_buffer_size=32768;
set max_length_for_sort_data=16;
/* 打开 optimizer_trace，只对本线程有效 */
SET optimizer_trace='enabled=on'; 

/* 执行语句 */
select word from words order by rand() limit 3;

/* 查看 OPTIMIZER_TRACE 输出 */
SELECT * FROM `information_schema`.`OPTIMIZER_TRACE`\G
```



问题：number_of_tmp_files 的值为什么是0

答案：filesort_priority_queue_optimization 这个部分的 chosen=true，就表示使用了优先队列排序算法，这个过程不需要临时文件，因此对应的 number_of_tmp_files 是 0。就是大顶堆的排序方式。



问题：下面语句为什么不用优先对了排序

```sql
select city,name,age from t where city='杭州' order by name limit 1000  ;
```

答案：堆的大小超过了sort_buffer_size 



## 13.3 随机排序法



### 13.3.1 方法一

1. 取得这个表的主键 id 的最大值 M 和最小值 N;
2. 用随机函数生成一个最大值到最小值之间的数 X = (M-N)*rand() + N;
3. 取不小于 X 的第一个 ID 的行。



问题：如果id中间有空洞，不同行的概率会不一样。



### 13.3.2 方法二

1. 取得整个表的行数，并记为 C。
2. 取得 Y = floor(C * rand())。 floor 函数在这里的作用，就是取整数部分。
3. 再用 limit Y,1 取得一行。



## 13.4 随机取三个单词

1. 取得整个表的行数，记为 C；
2. 根据相同的随机方法得到 Y1、Y2、Y3；
3. 再执行三个 limit Y, 1 语句得到三行数据。



## 13.5 总结

如果你直接使用 order by rand()，这个语句需要 Using temporary 和 Using filesort，查询的执行代价往往是比较大的。所以，在设计的时候你要尽量避开这种写法。尽量将业务逻辑写在业务代码中，让数据库只做“读写数据”的事情







# 第十四章 相同逻辑SQL语句性能分析

在 MySQL 中，有很多看上去逻辑相同，但性能却差异巨大的 SQL 语句。今天挑选了三个这样的案例和你分享



## 14.1 条件字段函数操作



### 14.1.1 表结构

```sql
CREATE TABLE `tradelog` (
  `id` int(11) NOT NULL,
  `tradeid` varchar(32) DEFAULT NULL,
  `operator` int(11) DEFAULT NULL,
  `t_modified` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `tradeid` (`tradeid`),
  KEY `t_modified` (`t_modified`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
```



### 14.1.2 查询语句

```sql
select count(*) from tradelog where month(t_modified)=7;
```

explain之后，发现扫描了索引的全部值。对索引字段做函数操作，可能会破坏索引值的有序性，因此优化器就决定放弃走树搜索功能。



### 14.1.3 正确sql语句

```sql
select count(*) from tradelog where
(t_modified >= '2016-7-1' and t_modified<'2016-8-1') or
(t_modified >= '2017-7-1' and t_modified<'2017-8-1') or 
(t_modified >= '2018-7-1' and t_modified<'2018-8-1');
```





## 14.2 隐式类型转换



### 14.2.1 查询语句

```sql
select * from tradelog where tradeid=110717;
```

tradeid 的字段类型是 varchar(32)，而输入的参数却是整型，所以需要做类型转换。这条语句触发了我们上面说到的规则：对索引字段做函数操作，优化器会放弃走树搜索功能。





## 14.3 隐式字符编码转换

两个表的字符集不同，一个是 utf8，一个是 utf8mb4，所以做表连接查询的时候用不上关联字段的索引。



### 14.3.1 表结构

```sql

CREATE TABLE `trade_detail` (
  `id` int(11) NOT NULL,
  `tradeid` varchar(32) DEFAULT NULL,
  `trade_step` int(11) DEFAULT NULL, /*操作步骤*/
  `step_info` varchar(32) DEFAULT NULL, /*步骤信息*/
  PRIMARY KEY (`id`),
  KEY `tradeid` (`tradeid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

insert into tradelog values(1, 'aaaaaaaa', 1000, now());
insert into tradelog values(2, 'aaaaaaab', 1000, now());
insert into tradelog values(3, 'aaaaaaac', 1000, now());

insert into trade_detail values(1, 'aaaaaaaa', 1, 'add');
insert into trade_detail values(2, 'aaaaaaaa', 2, 'update');
insert into trade_detail values(3, 'aaaaaaaa', 3, 'commit');
insert into trade_detail values(4, 'aaaaaaab', 1, 'add');
insert into trade_detail values(5, 'aaaaaaab', 2, 'update');
insert into trade_detail values(6, 'aaaaaaab', 3, 'update again');
insert into trade_detail values(7, 'aaaaaaab', 4, 'commit');
insert into trade_detail values(8, 'aaaaaaac', 1, 'add');
insert into trade_detail values(9, 'aaaaaaac', 2, 'update');
insert into trade_detail values(10, 'aaaaaaac', 3, 'update again');
insert into trade_detail values(11, 'aaaaaaac', 4, 'commit');
```



### 14.3.2 查询语句

```sql
select d.* from tradelog l, trade_detail d where d.tradeid=l.tradeid and l.id=2; /*语句Q1*/
```



explain结果

```sql
explain select d.* from tradelog l, trade_detail d where d.tradeid=l.tradeid and l.id=2; /*Q1*/


+----+-------------+-------+------------+-------+-----------------+---------+---------+-------+------+----------+-------------+
| id | select_type | table | partitions | type  | possible_keys   | key     | key_len | ref   | rows | filtered | Extra       |
+----+-------------+-------+------------+-------+-----------------+---------+---------+-------+------+----------+-------------+
|  1 | SIMPLE      | l     | NULL       | const | PRIMARY,tradeid | PRIMARY | 4       | const |    1 |   100.00 | NULL        |
|  1 | SIMPLE      | d     | NULL       | ALL   | NULL            | NULL    | NULL    | NULL  |   11 |   100.00 | Using where |
+----+-------------+-------+------------+-------+-----------------+---------+---------+-------+------+----------+-------------+
```

explain 的结果里面第二行的 key=NULL 表示的就是，这个过程是通过遍历主键索引的方式，一个一个地判断 tradeid 的值是否匹配



# 第十五章 只查一行也很慢

主题：在一个简单的表上，执行“查一行”，可能会出现的被锁住和执行慢的例子



构造表

```sql
CREATE TABLE `t` (
  `id` int(11) NOT NULL,
  `c` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;

delimiter ;;
create procedure idata5()
begin
  declare i int;
  set i=1;
  while(i<=100000) do
    insert into t values(i,i);
    set i=i+1;
  end while;
end;;
delimiter ;

call idata5();
```



## 15.1 查询长时间不返回



查询语句

```sql
select * from t where id=1;
```





### 15.1.1 等MDL锁

使用 show processlist 命令查看显示 Waiting for table metadata lock

```
mysql> show processlist;
+----+------+-----------+------+---------+------+---------------------------------+------------------------------+
| Id | User | Host      | db   | Command | Time | State                           | Info                         |
+----+------+-----------+------+---------+------+---------------------------------+------------------------------+
| 33 | root | localhost | test | Sleep   |   35 |                                 | NULL                         |
| 34 | root | localhost | test | Query   |   24 | Waiting for table metadata lock | select * from t where id = 1 |
| 35 | root | localhost | test | Query   |    0 | starting                        | show processlist             |
+----+------+-----------+------+---------+------+---------------------------------+------------------------------+
```



解决方案：就是找到谁持有 MDL 写锁，然后把它 kill 掉



```sql
select blocking_pid from sys.schema_table_lock_waits;

kill connection ${blocking_pid};
```



注意：该功能需要先开启与MDL锁等待事件相关的instruments:

```sql
update performance_schema.setup_instruments set  ENABLED='no',timed='no' where name like 'wait/lock/metadata/sql/mdl';

call sys.ps_setup_enable_instrument('wait/lock/metadata/sql/mdl');

+-----------------------+

| summary               |

+-----------------------+

| Enabled 1 instruments |

+-----------------------+

#显示1表示未开启
update performance_schema.setup_instruments set  ENABLED='yes',timed='yes' where name like 'wait/lock/metadata/sql/mdl';

select * from performance_schema.setup_instruments where name like 'wait/lock/metadata/sql/mdl';

+----------------------------+---------+-------+

| NAME                       | ENABLED | TIMED |

+----------------------------+---------+-------+

| wait/lock/metadata/sql/mdl | YES     | YES   |

+----------------------------+---------+-------+
-----------------------------------

call sys.ps_setup_enable_instrument('wait/lock/metadata/sql/mdl');

+-----------------------+

| summary               |

+-----------------------+

| Enabled 0 instruments |

+-----------------------+
```





### 15.1.2 等flush

flush表的操作有两个，正常这两个语句执行起来都很快，除非它们也被别的线程堵住了

```sql

flush tables t with read lock;

flush tables with read lock;
```



复现

| session A               | session B       | session C                     |
| ----------------------- | --------------- | ----------------------------- |
| select sleep(1) from t; |                 |                               |
|                         | flush tables t; |                               |
|                         |                 | select * from t where id = 1; |



```shell
mysql> show processlist;
+----+------+-----------+------+---------+------+-------------------------+------------------------------+
| Id | User | Host      | db   | Command | Time | State                   | Info                         |
+----+------+-----------+------+---------+------+-------------------------+------------------------------+
| 34 | root | localhost | test | Query   |   28 | Waiting for table flush | flush tables t               |
| 35 | root | localhost | test | Query   |   24 | Waiting for table flush | select * from t where id = 1 |
| 36 | root | localhost | test | Query   |   32 | User sleep              | select sleep(1) from t       |
| 37 | root | localhost | test | Query   |    0 | starting                | show processlist             |
+----+------+-----------+------+---------+------+-------------------------+------------------------------+
```



线程状态是：Waiting for table flush

把关键线程kill即可。



### 15.1.3 等行锁



复现

| session A                                 | session B                                        |
| ----------------------------------------- | ------------------------------------------------ |
| begin; update t set c = c+1 where id = 1; |                                                  |
|                                           | select * from t where id = 1 lock in share mode; |



show processlist

```shell
mysql> show processlist;
+----+------+-----------+------+---------+------+------------+-------------------------------------------------+
| Id | User | Host      | db   | Command | Time | State      | Info                                            |
+----+------+-----------+------+---------+------+------------+-------------------------------------------------+
| 34 | root | localhost | test | Query   |   24 | statistics | select * from t where id = 1 lock in share mode |
| 37 | root | localhost | test | Query   |    0 | starting   | show processlist                                |
| 42 | root | localhost | test | Sleep   |  154 |            | NULL                                            |
+----+------+-----------+------+---------+------+------------+-------------------------------------------------+

```

状态是：statistics



解决方案：查出谁占了写锁，然后kill即可

```sql
select * from sys.innodb_lock_waits where locked_table = '`test`.`t`' \G
```





## 15.2 查询慢



### 15.2.1 无索引，全表扫描

```sql
select * from t where c=50000 limit 1;
```



慢查询日志，扫描了5000行

```shell
# Time: 2022-10-10T08:23:28.690504Z
# User@Host: root[root] @ localhost []  Id:    43
# Query_time: 0.019780  Lock_time: 0.000119 Rows_sent: 1  Rows_examined: 50000
SET timestamp=1665390208;
select * from t where c=50000 limit 1;
```





### 15.2.2 一致性读多次执行undo log



复现

| session A                                        | session B                                |
| ------------------------------------------------ | ---------------------------------------- |
| start transaction with consistent snapshot；     |                                          |
|                                                  | update t set c=c+1 where id=1;执行一万次 |
| select * from t where id=1;                      |                                          |
| select * from t where id = 1 lock in share mode; |                                          |



带 lock in share mode 的 SQL 语句，是当前读，因此会直接读到 1000001 这个结果，所以速度很快；而 select * from t where id=1 这个语句，是一致性读，因此需要从 1000001 开始，依次执行 undo log，执行了 100 万次以后，才将 1 这个结果返回



```
select * from t where id=1 扫描行数为1,时间却长达30ms

# Query_time: 0.030567  Lock_time: 0.000159 Rows_sent: 1  Rows_examined: 1
SET timestamp=1665391329;
select * from t where id=1;

```







# 第十六章 幻读[难点]





# 第十七章 行锁[难点]





# 第十八章 临时提升MySQL性能



## 18.1 短连接风暴

短连接超过这个max_connections，系统就会拒绝接下来的连接请求，并报错提示“Too many connections。



会话

|         | session A                       | session B                     | session C         |
| ------- | ------------------------------- | ----------------------------- | ----------------- |
| T       | begin;insert into t values(1,1) | select * from t where id = 1; |                   |
| T + 30s |                                 |                               | show processlist; |



### 18.1.1 处理掉空闲线程

1. 查看线程状态，其中Command 为 Sleep的是空闲线程

   ```shell
   +----+------+-----------+------+---------+------+----------+------------------+
   | Id | User | Host      | db   | Command | Time | State    | Info             |
   +----+------+-----------+------+---------+------+----------+------------------+
   | 22 | root | localhost | test | Sleep   |   52 |          | NULL             |
   | 23 | root | localhost | test | Sleep   |   27 |          | NULL             |
   | 24 | root | localhost | test | Query   |    0 | starting | show processlist |
   +----+------+-----------+------+---------+------+----------+------------------+
   ```

2. 优先断开像 session B 这样的事务外空闲的连接

   ```sql
   #查看事务内空闲线程
   select * from information_schema.innodb_trx \G
   
   *************************** 1. row ***************************
                       trx_id: 362790
                    trx_state: RUNNING
                  trx_started: 2022-10-10 03:26:09
        trx_requested_lock_id: NULL
             trx_wait_started: NULL
                   trx_weight: 2
          trx_mysql_thread_id: 22
                    trx_query: NULL
          trx_operation_state: NULL
            trx_tables_in_use: 0
            trx_tables_locked: 1
             trx_lock_structs: 1
        trx_lock_memory_bytes: 1136
              trx_rows_locked: 0
            trx_rows_modified: 1
      trx_concurrency_tickets: 0
          trx_isolation_level: REPEATABLE READ
            trx_unique_checks: 1
       trx_foreign_key_checks: 1
   trx_last_foreign_key_error: NULL
    trx_adaptive_hash_latched: 0
    trx_adaptive_hash_timeout: 0
             trx_is_read_only: 0
   trx_autocommit_non_locking: 0
   
   trx_mysql_thread_id: 22 表示22号线程处于事务中,所以先断开23号线程
   ```

3. 断开线程

   ```shell
    kill connection + id 
   ```

   



### 18.1.2 减少连接过程的消耗

跳过权限验证的方法是：重启数据库，并使用–skip-grant-tables 参数启动





### 18.1.3 调高 max_connections 的值

max_connections 这个参数的目的是想保护 MySQL，如果我们把它改得太大，让更多的连接都可以进来，那么系统的负载可能会进一步加大，大量的资源耗费在权限验证等逻辑上，结果可能是适得其反，已经连接的线程拿不到 CPU 资源去执行业务的 SQL 请求



## 18.2 慢查询





### 18.2.1 索引没设计好

紧急创建索引来解决。假设服务是一主一备，主库 A、备库 B，这个方案的大致流程是这样的

1. 在备库 B 上执行 set sql_log_bin=off，也就是不写 binlog，然后执行 alter table 语句加上索引；
2. 执行主备切换；
3. 这时候主库是 B，备库是 A。在 A 上执行 set sql_log_bin=off，然后执行 alter table 语句加上索引。



### 18.2.2 SQL语句没写好

MySQL 5.7 提供了 query_rewrite 功能，可以把输入的一种语句改写成另外一种模式。比如下面的语句可以将如下sql修改

```sql
 select * from t where id + 1 = 10000
```



修改方法

```sql
insert into query_rewrite.rewrite_rules(pattern, replacement, pattern_database) values ("select * from t where id + 1 = ?", "select * from t where id = ? - 1", "db1");

call query_rewrite.flush_rewrite_rules();
```



注意：query_rewrite 是MySQL 5.7.6之后的版本才支持的功能。

安装query_rewrite 

```shell
mysql -uroot -p'tars2015' < /usr/share/mysql/install_rewriter.sql
```









### 18.2.3 MySQL选错索引

使用查询重写功能，给原来的语句加上 force index





### 18.2.4 预先发现问题

1. 上线前，在测试环境，把慢查询日志（slow log）打开，并且把 long_query_time 设置成 0，确保每个语句都会被记录入慢查询日志
2. 在测试表里插入模拟线上的数据，做一遍回归测试
3. 观察慢查询日志里每类语句的输出，特别留意 Rows_examined 字段是否与预期一致







## 18.3 QPS突增

线上新功能，该功能有Bug导致QPS突增。



解决方案：下架新功能

+ 一种是由全新业务的 bug 导致的。假设你的 DB 运维是比较规范的，也就是说白名单是一个个加的。这种情况下，如果你能够确定业务方会下掉这个功能，只是时间上没那么快，那么就可以从数据库端直接把白名单去掉
+ 如果这个新功能使用的是单独的数据库用户，可以用管理员账号把这个用户删掉，然后断开现有连接。这样，这个新功能的连接不成功，由它引发的 QPS 就会变成 0。
+ 如果这个新增的功能跟主体功能是部署在一起的，那么我们只能通过处理语句来限制。这时，我们可以使用上面提到的查询重写功能，把压力最大的 SQL 语句直接重写成"select 1"返回。



# 第二十三章 如何保证数据不丢失





# 第二十四章 如何保证主备一致





# 第二十五章 高可用





# 第二十六章 备库延迟



# 第二十七章 主库出问题，从库怎么办



# 第三十四章 到底可不可以使用join

问题：

1. DBA 不让使用 join，使用 join 有什么问题呢
2. 如果有两个大小不同的表做 join，应该用哪个表做驱动表呢



建表

```sql
CREATE TABLE `t2` (
  `id` int(11) NOT NULL,
  `a` int(11) DEFAULT NULL,
  `b` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `a` (`a`)
) ENGINE=InnoDB;

drop procedure idata;
delimiter ;;
create procedure idata()
begin
  declare i int;
  set i=1;
  while(i<=1000)do
    insert into t2 values(i, i, i);
    set i=i+1;
  end while;
end;;
delimiter ;
call idata();

create table t1 like t2;
insert into t1 (select * from t2 where id<=100);
```





## 34.1 Index Nested-Loop Join

查询语句

```sql
/*straight_join 让 MySQL 使用固定的连接方式执行查询*/
select * from t1 straight_join t2 on (t1.a=t2.a);
```



执行流程

1. 从表 t1 中读入一行数据 R
2. 从数据行 R 中，取出 a 字段到表 t2 里去查找
3. 取出表 t2 中满足条件的行，跟 R 组成一行，作为结果集的一部分
4. 重复执行步骤 1 到 3，直到表 t1 的末尾循环结束



结论：

1. 使用 join 语句，性能比强行拆成多个单表执行 SQL 语句的性能要好
2. 如果使用 join 语句的话，需要让小表做驱动表
3. 前提：可以使用被驱动表的索引





## 34.2 Simple Nested-Loop Join

SQL语句

```sql
select * from t1 straight_join t2 on (t1.a=t2.b);
```

由于表 t2 的字段 b 上没有索引，因此再用图 2 的执行流程时，每次到 t2 去匹配的时候，就要做一次全表扫描。这样算来，这个 SQL 请求就要扫描表 t2 多达 100 次，总共扫描 100*1000=10 万行。



## 34.3 Block Nested-Loop Join

算法流程：

1. 把表 t1 的数据读入线程内存 join_buffer 中，由于我们这个语句中写的是 select *，因此是把整个表 t1 放入了内存
2. 扫描表 t2，把表 t2 中的每一行取出来，跟 join_buffer 中的数据做对比，满足 join 条件的，作为结果集的一部分返回



如果表t1太大，join_buffer 无法放下全部，就分段放。执行过程变成：

1. 扫描表 t1，顺序读取数据行放入 join_buffer 中，放完第 88 行 join_buffer 满了，继续第 2 步
2. 扫描表 t2，把 t2 中的每一行取出来，跟 join_buffer 中的数据做对比，满足 join 条件的，作为结果集的一部分返回
3. 清空 join_buffer
4. 继续扫描表 t1，顺序读取最后的 12 行数据放入 join_buffer 中，继续执行第 2 步



如果join太慢就把参数join_buffer_size 调大，默认是256k，可以调整到16m。



## 34.5 总结

1. 如果可以使用 Index Nested-Loop Join 算法，也就是说可以用上被驱动表上的索引，可以使用join
2. 如果使用 Block Nested-Loop Join 算法，扫描行数就会过多。尤其是在大表上的 join 操作，这样可能要扫描被驱动表很多次，会占用大量的系统资源。所以这种 join 尽量不要用。explain是，extra字段有关键词Block Nested Loop
3. 应该使用小表做驱动表
4. 小表是指：两个表按照各自的条件过滤，过滤完成之后，计算参与 join 的各个字段的总数据量





# 第三十六章 join语句怎么优化

建表

```sql
create table t1(id int primary key, a int, b int, index(a));
create table t2 like t1;
drop procedure idata;
delimiter ;;
create procedure idata()
begin
  declare i int;
  set i=1;
  while(i<=1000)do
    insert into t1 values(i, 1001-i, i);
    set i=i+1;
  end while;
  
  set i=1;
  while(i<=1000000)do
    insert into t2 values(i, i, i);
    set i=i+1;
  end while;

end;;
delimiter ;
call idata();
```





## 36.1 Multi-Range Read 优化

查询语句

```sql
select * from t1 where a>=1 and a<=100;
```

InnoDB 在普通索引 a 上查到主键 id 的值后，再根据一个个主键 id 的值到主键索引上去查整行数据。随着 a 的值递增顺序查询的话，id 的值就变成随机的，那么就会出现随机访问，性能相对较差。



优化思路：

1. 根据索引 a，定位到满足条件的记录，将 id 值放入 read_rnd_buffer 中
2. 将 read_rnd_buffer 中的 id 进行递增排序
3. 排序后的 id 数组，依次到主键 id 索引中查记录，并作为结果返回



使用MRR优化

```sql
set optimizer_switch="mrr_cost_based=off";

/*Extra 里多出MRR*/
explain select * from t1 where a>=1 and a<=100;
```







## 36.2 Batched Key Access

NLJ 算法执行的逻辑是：从驱动表 t1，一行行地取出 a 的值，再到被驱动表 t2 去做 join。也就是说，对于表 t2 来说，每次都是匹配一个值。我们就把表 t1 的数据取出来一部分，先放到一个临时内存join_buffer。



开启BKA优化，执行SQL语句前，先设置

```sql
set optimizer_switch='mrr=on,mrr_cost_based=off,batched_key_access=on';
```





## 36.3 BNL性能问题

1. 可能会多次扫描被驱动表，占用磁盘 IO 资源
2. 判断 join 条件需要执行 M*N 次对比（M、N 分别是两张表的行数），如果是大表就会占用非常多的 CPU 资源；
3. 可能会导致 Buffer Pool 的热数据被淘汰，影响内存命中率



## 36.4 BNL 转 BKA 



### 36.4.1 方法一

直接在被驱动表上建索引，就能转成BKA了



### 36.4.2 方法二

1. 把表 t2 中满足条件的数据放在临时表 tmp_t 中
2. 为了让 join 使用 BKA 算法，给临时表 tmp_t 的字段 b 加上索引
3. 让表 t1 和 tmp_t 做 join 操作



对应SQL

```sql

create temporary table temp_t(id int primary key, a int, b int, index(b))engine=innodb;
insert into temp_t select * from t2 where b>=1 and b<=2000;
select * from t1 join temp_t on (t1.b=temp_t.b);
```





## 36.5 拓展 hash join

思路：oin_buffer 里面维护的不是一个无序数组，而是一个哈希表的话，这样相等判断会很快



1. select * from t1;取得表 t1 的全部 1000 行数据，在业务端存入一个 hash 结构，比如 C++ 里的 set、PHP 的数组这样的数据结构
2. select * from t2 where b>=1 and b<=2000; 获取表 t2 中满足条件的 2000 行数据
3. 把这 2000 行数据，一行一行地取到业务端，到 hash 结构的数据表中寻找匹配的数据。满足匹配的条件的这行数据，就作为结果集的一行



# 第三十六章 为什么临时表可以重名



## 36.1 临时表和内存表的区别

+ 内存表，指的是使用 Memory 引擎的表，建表语法是 create table … engine=memory。这种表的数据都保存在内存里，系统重启的时候会被清空，但是表结构还在
+ 临时表，可以使用各种引擎类型 。如果是使用 InnoDB 引擎或者 MyISAM 引擎的临时表，写数据的时候是写到磁盘上的。当然，临时表也可以使用 Memory 引擎





## 36.2 临时表的特征

1. 建表语法是 create temporary table …。
2. 一个临时表只能被创建它的 session 访问，对其他线程不可见
3. 不同 session 的临时表是可以重名的，如果有多个 session 同时执行 join 优化，不需要担心表名重复导致建表失败的问题
4. 不需要担心数据删除问题。临时表由于会自动回收，所以不需要这个额外的操作



## 36.3 临时表的应用

典型常见：分库分表系统的跨库查询。



分库分表：把逻辑上的大表分散到不同的数据库实例上。



问题：表通过字段f分区分表，但是查询时没用到字段f

```sql
select v from ht where k >= M order by t_modified desc limit 100;
```



### 36.3.1 解决方案一

在 proxy 层的进程代码中实现排序。proxy层拿到分库的数据以后，直接在内存中参与计算。



### 36.3.3 解决方案二

把各个分库拿到的数据，汇总到一个 MySQL 实例的一个表中，然后在这个汇总实例上做逻辑操作。

1. 把临时表 temp_ht 放到 32 个分库中的某一个计算不包含的上

2. 在各个分库上执行

   ```sql
   select v,k,t_modified from ht_x where k >= M order by t_modified desc limit 100;
   ```

3. 把分库执行的结果插入到 temp_ht 表中

4. 执行

   ```sql
   select v from temp_ht order by t_modified desc limit 100; 
   ```



## 36.4 为什么临时表可以重名



查看临时表存放目录

```sql
select @@tmpdir;
```



临时表磁盘文件命名规则

```ini
rule = #sql{进程 id}_{线程 id}_ 序列号.frm
example = #sql1_f_0.frm
```



临时表内存命名规则

```ini
rule = 库民 +  表名 + server_id+thread_id
detail = 每个线程都维护了自己的临时表链表。这样每次 session 内操作表的时候，先遍历链表，检查是否有这个名字的临时表，如果有就优先操作临时表，如果没有再操作普通表；在 session 结束的时候，对链表里的每个临时表，执行 “DROP TEMPORARY TABLE + 表名”操作
```



## 36.5 临时表和主备复制

1. binlog_format=row，那么跟临时表有关的语句，就不会记录到 binlog 里。

2. binlog_format=statment/mixed 的时候，binlog 中才会记录临时表的操作

   ```sql
   
   create table t_normal(id int primary key, c int)engine=innodb;/*Q1*/
   create temporary table temp_t like t_normal;/*Q2*/
   insert into temp_t values(1,1);/*Q3*/
   insert into t_normal select * from temp_t;/*Q4*/
   
   #session结束的时候,对链表里面的每个临时表,执行 “DROP TEMPORARY TABLE + 表名”操作,传给备库
   ```



问题：主库上不同的线程创建同名的临时表是没关系的，但是传到备库执行是怎么处理的呢

答案：

+ session A 的临时表 t1，在备库的 table_def_key 就是：库名 +t1+“M 的 serverid”+“session A 的 thread_id“
+ session B 的临时表 t1，在备库的 table_def_key 就是 ：库名 +t1+“M 的 serverid”+“session B 的 thread_id“

由于 table_def_key 不同，所以这两个表在备库的应用线程里面是不会冲突的





# 第三十七章 什么时候会使用临时表



## 37.1 union执行流程

建表

```sql

create table t1(id int primary key, a int, b int, index(a));
delimiter ;;
create procedure idata()
begin
  declare i int;

  set i=1;
  while(i<=1000)do
    insert into t1 values(i, i, i);
    set i=i+1;
  end while;
end;;
delimiter ;
call idata();
```



执行语句

```sql

(select 1000 as f) union (select id from t1 order by id desc limit 2);
```



分析语句

```sql
explain (select 1000 as f) union (select id from t1 order by id desc limit 2);
```



语句执行流程分析

1. 创建一个内存临时表，这个临时表只有一个整型字段 f，并且 f 是主键字段
2. 执行第一个子查询，得到 1000 这个值，并存入临时表中
3. 执行第二个子查询
   + 拿到第一行 id=1000，试图插入临时表中。但由于 1000 这个值已经存在于临时表了，违反了唯一性约束，所以插入失败，然后继续执行
   + 取到第二行 id=999，插入临时表成功
4. 从临时表中按行取出数据，返回结果，并删除临时表，结果中包含两行数据分别是 1000 和 999



## 37.2 group by 执行流程



```sql
select id%10 as m, count(*) as c from t1 group by m;
```



explain

```ini
[Extra字段]
Using index     = 语句使用了覆盖索引，选择了索引 a，不需要回表
Using temporary = 使用了临时表
Using filesor   = 需要排序。
```



执行流程分析

1. 创建内存临时表，表里有两个字段 m 和 c，主键是 m
2. 扫描表 t1 的索引 a，依次取出叶子节点上的 id 值，计算 id%10 的结果，记为 x
   + 如果临时表中没有主键为 x 的行，就插入一个记录 (x,1);
   + 如果表中有主键为 x 的行，就将 x 这一行的 c 值加 1
3. 遍历完成后，再根据字段 m 做排序，得到结果集返回给客户端



如果在sql语句后加上order by null，就没有了排序阶段

```sql
select id%10 as m, count(*) as c from t1 group by m order by null;
```



## 37.3 group by 优化



优化思路：在字段上增加索引。MySQL 5.7 版本支持了 generated column 机制，用来实现列数据的关联更新。

```sql
alter table t1 add column z int generated always as(id % 100), add index(z);
```



上面的sql语句改为

```sql
select z, count(*) as c from t1 group by z;
```



Explain

```ini
[Extra]
Using index = 语句使用了覆盖索引，选择了索引 a，不需要回表
```



## 37.4 group by 优化 -- 直接排序

如果碰到不适合加索引的常见，并且需要放到临时表上的数据量特别大，让MySQL 有没有让我们直接走磁盘临时表。



```sql
select SQL_BIG_RESULT id%100 as m, count(*) as c from t1 group by m;
```



如果数据量不是特别大，适当调整参数tmp_table_size ，来尽量使用内存临时表。



增大**sort_buffer_size**的大小，Mysql执行order by 操作时，需要用到sort_buffer。





# 第三十九章  自增主键不连续



表结构

```sql
CREATE TABLE `t` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c` int(11) DEFAULT NULL,
  `d` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `c` (`c`)
) ENGINE=InnoDB;
```



## 39.1 自增主键保存场所



插入记录

```sql
insert into t values(null, 1, 1); 
```



查看

```sql
mysql> show  create table t \G;
*************************** 1. row ***************************
       Table: t
Create Table: CREATE TABLE `t` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `c` int(11) DEFAULT NULL,
  `d` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `c` (`c`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=latin1
1 row in set (0.00 sec)

```



保存位置

+ MyISAM 引擎的自增值保存在数据文件中
+ InnoDB 引擎的自增值，在 MySQL 5.7 及之前的版本，自增值保存在内存里，并没有持久化。每次重启后，第一次打开表的时候，都会去找自增值的最大值 max(id)，然后将 max(id)+1 作为这个表当前的自增值。在 MySQL 8.0 版本，将自增值的变更记录在了 redo log 中，重启的时候依靠 redo log 恢复重启之前的值





## 39.2 自增值修改机制



### 39.2.1 自增值行为

1. 如果插入数据时 id 字段指定为 0、null 或未指定值，那么就把这个表当前的 AUTO_INCREMENT 值填到自增字段
2. 如果插入数据时 id 字段指定了具体的值，就直接使用语句里指定的值



### 39.2.2 自增值变更

根据要插入的值和当前自增值的大小关系，自增值的变更结果也会有所不同。假设，某次要插入的值是 X，当前的自增值是 Y。

1. 如果 X<Y，那么这个表的自增值不变
2. 如果 X≥Y，就需要把当前自增值修改为新的自增值





## 39.3 自增值修改时机

假设，表 t 里面已经有了 (1,1,1) 这条记录，这时我再执行一条插入数据命令

```sql
insert into t values(null, 1, 1); 
```

1. 执行器调用 InnoDB 引擎接口写入一行，传入的这一行的值是 (0,1,1);
2. InnoDB 发现用户没有指定自增 id 的值，获取表 t 当前的自增值 2；
3. 将传入的行的值改成 (2,1,1);
4. 将表的自增值改成 3；
5. 继续执行插入数据操作，由于已经存在 c=1 的记录，所以报 Duplicate key error，语句返回。





**结论：唯一键冲突是导致自增主键 id 不连续的第一种原因**



事务回滚也会导致自增id不连续

```sql
insert into t values(null,1,1);
begin;
insert into t values(null,2,2);
rollback;
insert into t values(null,2,2);
//插入的行是(3,2,2)
```







**结论：事务回滚是导致自增主键 id 不连续的第二种原因**





## 39.4 自增锁的优化



优化参数innodb_autoinc_lock_mode

1. 这个参数的值被设置为 0 时，表示采用之前 MySQL 5.0 版本的策略，即语句执行结束后才释放锁
2. 这个参数的值被设置为 1 时
   + 普通 insert 语句，自增锁在申请之后就马上释放
   + 类似 insert … select 这样的批量插入数据的语句，自增锁还是要等语句结束后才被释放；
3. 这个参数的值被设置为 2 时，所有的申请自增主键的动作都是申请后就释放锁

**默认值是1。**



自增id分配策略

1. 在普通的 insert 语句里面包含多个 value 值的情况下，即使 innodb_autoinc_lock_mode 设置为 1，也不会等语句执行完成才释放锁。因为这类语句在申请自增 id 的时候，是可以精确计算出需要多少个 id 的，然后一次性申请，申请完成后锁就可以释放了

2. 对于批量插入数据的语句，不知道要预先申请多少个 id，MySQL 有一个批量申请自增 id 的策略

   + 语句执行过程中，第一次申请自增 id，会分配 1 个；

   + 1 个用完以后，这个语句第二次申请自增 id，会分配 2 个；

   + 2 个用完以后，还是这个语句，第三次申请自增 id，会分配 4 个；

   + 依此类推，同一个语句去申请自增 id，每次申请到的自增 id 个数都是上一次的两倍。

   + 例子

     ```sql
     insert into t values(null, 1,1);
     insert into t values(null, 2,2);
     insert into t values(null, 3,3);
     insert into t values(null, 4,4);
     create table t2 like t;
     insert into t2(c,d) select c,d from t;
     insert into t2 values(null, 5,5);
     
     由于这条语句实际只用上了 4 个 id，所以 id=5 到 id=7 就被浪费掉了。之后，再执行 insert into t2 values(null, 5,5)，实际上插入的数据就是（8,5,5)
     ```



**结论：批量插入数据会导致自增id不连续**





## 39.5 自增主键不连续的原因

1. 唯一键冲突

2. 事务回滚

3. 批量插入数据

   ```ini
   [sql-1]
   state = insert … select、
   
   [sql-2]
   state = replace … select
   
   [sql-3]
   state = load data
   ```



建议：在生产上，尤其是有 insert … select 这种批量插入数据的场景时，从并发插入数据性能的角度考虑，我建议你这样设置：innodb_autoinc_lock_mode=2 ，并且 binlog_format=row







# 第四十一章 快速复制一张表



表结构

```sql
create database db1;
use db1;

create table t(id int primary key, a int, b int, index(a))engine=innodb;
delimiter ;;
  create procedure idata()
  begin
    declare i int;
    set i=1;
    while(i<=1000)do
      insert into t values(i,i,i);
      set i=i+1;
    end while;
  end;;
delimiter ;
call idata();

create database db2;
create table db2.t like db1.t
```





## 41.1 mysqldump



### 41.1.1 导出数据

```sql
mysqldump -h$host -P$port -u$user -p --add-locks=0 --no-create-info --single-transaction  --set-gtid-purged=OFF db1 t --where="a>900" --result-file=/client_tmp/t.sql
```

1. --single-transaction 的作用是，在导出数据的时候不需要对表 db1.t 加表锁，而是使用 START TRANSACTION WITH CONSISTENT SNAPSHOT 的方法；
2. --add-locks 设置为 0，表示在输出的文件结果里，不增加" LOCK TABLES t WRITE;" 
3. --no-create-info 的意思是，不需要导出表结构；
4. --set-gtid-purged=off 表示的是，不输出跟 GTID 相关的信息；
5. --result-file 指定了输出文件的路径，其中 client 表示生成的文件是在客户端机器上的。
6. --where指定了过滤条件



### 41.1.2 导入数据

```sql
mysql -h127.0.0.1 -P13000  -uroot db2 -e "source /client_tmp/t.sql"
```

1. 打开文件，默认以分号为结尾读取一条条的 SQL 语句；
2. 将 SQL 语句发送到服务端执行。









## 41.2 csv



相关参数

```ini
[secure_file_priv ]
desc = 指定csv文件生成的根目录
;select @@secure_file_priv;
default value = /var/lib/mysql-files/
```



### 41.2.1 导出数据

```sql
select * from db1.t where a>900 into outfile '/var/lib/mysql-files/t.csv';
```

说明

1. 这条语句会将结果保存在服务端。
2. into outfile 指定了文件的生成位置，这个位置必须受参数 secure_file_priv 的限制
   + 如果设置为 empty，表示不限制文件生成的位置，这是不安全的设置
   + 如果设置为一个表示路径的字符串，就要求生成的文件只能放在这个指定的目录，或者它的子目录，默认是/var/lib/mysql-files/
   + 如果设置为 NULL，就表示禁止在这个 MySQL 实例上执行 select … into outfile 操作
3. 这条命令不会帮你覆盖文件，因此你需要确保 /server_tmp/t.csv 这个文件不存在，否则执行语句时就会因为有同名文件的存在而报错



注意：select …into outfile 方法不会生成表结构文件, 所以我们导数据时还需要单独的命令得到表结构定义

```sql
mysqldump -h$host -P$port -u$user ---single-transaction  --set-gtid-purged=OFF db1 t --where="a>900" --tab=$secure_file_priv
```



### 41.2.2 导入数据

```sql
load data infile '/var/lib/mysql-files/t.csv' into table db2.t;
```





### 41.2.3 load data的用法

1. 不加“local”，是读取服务端的文件，这个文件必须在 secure_file_priv 指定的目录或子目录下；
2. 加上“local”，读取的是客户端的文件，只要 mysql 客户端有访问这个文件的权限即可。这时候，MySQL 客户端会先把本地文件传给服务端，然后执行上述的 load data 流程。







## 41.3 物理拷贝



问题：直接把 db1.t 表的.frm 文件和.ibd 文件拷贝到 db2 目录下，是否可行呢？

答案：不行。一个 InnoDB 表，除了包含这两个物理文件外，还需要在数据字典中注册。直接拷贝这两个文件的话，因为数据字典中没有 db2.t 这个表，系统是不会识别和接受它们的。MySQL  5.6引入了可传输表空间(transportable tablespace) 的方法，可以通过导出 + 导入表空间的方式，实现物理拷贝表的功能





假设我们现在的目标是在 db1 库下，复制一个跟表 t 相同的表 r，具体的执行步骤如下

1. 执行 create table r like t，创建一个相同表结构的空表
2. 执行 alter table r discard tablespace，这时候 r.ibd 文件会被删除
3. 执行 flush table t for export，这时候 db1 目录下会生成一个 t.cfg 文件
4. 在 db1 目录下执行 cp t.cfg r.cfg; cp t.ibd r.ibd；这两个命令，修改文件权限chown mysql:mysql r.ibd + chown mysql:mysql r.cfg
5. 执行 unlock tables，这时候 t.cfg 文件会被删除
6. 执行 alter table r import tablespace，将这个 r.ibd 文件作为表 r 的新的表空间，由于这个文件的数据内容和 t.ibd 是相同的，所以表 r 中就有了和表 t 相同的数据







## 41.4 总结

1. 物理拷贝的方式速度最快，尤其对于大表拷贝来说是最快的方法。但是使用也有一定的局限性
   + 必须是全表拷贝，不能只拷贝部分数据
   + 需要到服务器上拷贝数据，在用户无法登录数据库主机的场景下无法使用
   + 由于是通过拷贝物理文件实现的，源表和目标表都是使用 InnoDB 引擎时才能使用
2. 用 mysqldump 生成包含 INSERT 语句文件的方法，可以在 where 参数增加过滤条件，来实现只导出部分数据。这个方式的不足之一是，不能使用 join 这种比较复杂的 where 条件写法
3. 用 select … into outfile 的方法是最灵活的，支持所有的 SQL 写法。但，这个方法的缺点之一就是，每次只能导出一张表的数据，而且表结构也需要另外的语句单独备份，必须登录到服务器。







## 41.5 导出整个数据库

```shell
mysqldump -h$host -P$port -u$user -p --add-locks=0 --no-create-info --single-transaction  --set-gtid-purged=OFF $db --result-file=/opt/$db.sql
```

上面的命令不导出表结构，如果需要导出表结构把参数--no-create-info 去掉。





# 第四十二章 权限配置



## 42.1 问题

+ grant 之后真的需要执行 flush privileges 吗
+ 如果没有执行这个 flush 命令的话，赋权语句真的不能生效吗



创建用户

```ini
[创建用户]
cmd  = create user 'ua'@'%' identified by 'pa';
desc = 在 MySQL 里面，用户名 (user)+ 地址 (host) 才表示一个用户，因此 ua@ip1 和 ua@ip2 代表的是两个不同的用户。%表示所有Ip地址

;刚安装数据库时,root用户只能localhost访问
;增加一个特定ip的root用户
;mysql的用户名是名字 +Ip 组成的
cmd = create user 'root'@'18.231.132.46' identified by 'qhx#2TD3WR+b1sMa';
;授权特定的数据库
cmd = grant all privileges on machine_game.* to 'root'@'18.231.132.46' with grant option;

;查询账号信息
cmd = select host, user from mysql.user;
```





## 42.2 全局权限

全局权限保存在mysql.user中

```mysql
select * from mysql.user where user = 'ua' \G
```





### 42.2.1 赋予权限

```mysql
grant all privileges on *.* to 'ua'@'%' with grant option;
```

1. grant 命令对于全局权限，同时更新了磁盘和内存。命令完成后即时生效，接下来新创建的连接会使用新的权限
2. 对于一个已经存在的连接，它的全局权限不受 grant 命令的影响
3. 在生产环境上要合理控制用户权限的范围，如果一个用户有所有权限，一般就不应该设置为所有 IP 地址都可以访问。



### 42.2.2 移除权限

```mysql
revoke all privileges on *.* from 'ua'@'%';
```





## 42.3 DB权限

除了全局权限，MySQL 也支持库级别的权限定义。如果要让用户 ua 拥有库 db1 的所有权限，可以执行下面这条命令

```mysql
grant all privileges on db1.* to 'ua'@'%' with grant option;
```



基于库的权限记录保存在 mysql.db 表中

```mysql
select * from mysql.db where user = 'ua' \G
```







## 42.4 表权限和列权限

表权限定义存放在表 mysql.tables_priv 中，列权限定义存放在表 mysql.columns_priv 中。这两类权限，组合起来存放在内存的 hash 结构 column_priv_hash 中



赋予权限的命令

```mysql

create table db1.t1(id int, a int);

grant all privileges on db1.t1 to 'ua'@'%' with grant option;
GRANT SELECT(id), INSERT (id,a) ON mydb.mytbl TO 'ua'@'%' with grant option;
```



## 42.5 结论

1. 如果我们都是用 grant/revoke 语句来执行的话，内存和数据表本来就是保持同步更新的，不需要执行 flush privileges
2. flush privileges 命令会清空 acl_users 数组，然后从 mysql.user 表中读取数据重新加载，重新构造一个 acl_users 数组。也就是说，以数据表中的数据为准，会将全局权限内存数组重新加载一遍





## 42.6 flush privileges的使用场景

当数据表中的权限数据跟内存中的权限数据不一致的时候，flush privileges 语句可以用来重建内存数据，达到一致状态



比如直接修改表的数据管理权限

```mysql
delete from mysql.user where user='ua';
flush privileges;
```





## 42.7 其它命令



删除用户

```mysql
DROP USER 'api@localhost';
```







# 第四十三章 分区表





## 43.1 分区类型

| 分区类型   | 使用频率                        |
| ---------- | ------------------------------- |
| RANGE 分区 | 较多                            |
| HASH 分区  | 较多，适合游戏开发，根据uid分区 |
| LIST 分区  | 一般                            |
| KEYS 分区  | 一般                            |



range分区

```mysql
CREATE TABLE `t` (
  `ftime` datetime NOT NULL,
  `c` int(11) DEFAULT NULL,
  KEY (`ftime`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1
PARTITION BY RANGE (YEAR(ftime))
(PARTITION p_2017 VALUES LESS THAN (2017) ENGINE = InnoDB,
 PARTITION p_2018 VALUES LESS THAN (2018) ENGINE = InnoDB,
 PARTITION p_2019 VALUES LESS THAN (2019) ENGINE = InnoDB,
PARTITION p_others VALUES LESS THAN MAXVALUE ENGINE = InnoDB);
insert into t values('2017-4-1',1),('2018-4-1',1);
```



hash分区

```mysql
#常规的hash分区使用的是取模的算法
CREATE TABLE employees (
    id INT NOT NULL,
    fname VARCHAR(30),
    lname VARCHAR(30),
    hired DATE NOT NULL DEFAULT '1970-01-01',
    separated DATE NOT NULL DEFAULT '9999-12-31',
    job_code INT,
    store_id INT
)
PARTITION BY HASH(store_id)
PARTITIONS 4;
```





## 43.2 分区表的引擎层行为



### 43.2.1 Innodb

|      | Session A                                            | Session B                                    |
| ---- | ---------------------------------------------------- | -------------------------------------------- |
| T1   | begin;                                               |                                              |
| T2   | select * from t wherer ftime = '2017-5-1' for update |                                              |
| T3   |                                                      | insert into t values('2018-2-1',1); [ok]     |
|      |                                                      |                                              |
|      |                                                      | insert into t values('2017-12-1',1); [block] |



结论：在Innodb引擎层，认为分区表是两个表，不是一个单独的表。





### 43.2.2 MyISAM



| Session A                                         | Session B                                         |
| ------------------------------------------------- | ------------------------------------------------- |
| alter table t engine = myisam;                    |                                                   |
| update t set c=sleep(100) where ftime='2017-4-1'; |                                                   |
|                                                   | select * from t where ftime='2018-4-1'; [OK]      |
|                                                   | select * from t where ftime='2017-5-1'; [blocked] |

结论：在myisam引擎层，认为分区表是两个表，不是一个单独的表。







## 43.3 手动分表和分区表的区别



### 43.3.1 分区策略

每当第一次访问一个分区表的时候，MySQL 需要把所有的分区都访问一遍。一个典型的报错情况是这样的：如果一个分区表的分区很多，比如超过了 1000 个，而 MySQL 启动的时候，open_files_limit 参数使用的是默认值 1024，那么就会在访问这个表的时候，由于需要打开所有的文件，导致打开表文件的个数超过了上限而报错。注意：**InnoDB 引擎不存在这个问题**





### 43.3.2 分区表的server层行为

|      | Session A                               | Session B                                        |
| ---- | --------------------------------------- | ------------------------------------------------ |
| T1   | begin;                                  |                                                  |
| T2   | select * from t where ftime='2018-4-1'; |                                                  |
| T3   |                                         | alter table t truncate partition p_2017; [block] |

当需要truncate 一个分表的时候，会出现MDL锁冲突。





### 43.3.3 总结

1. MySQL 在第一次打开分区表的时候，需要访问所有的分区
2. 在 server 层，认为这是同一张表，因此所有分区共用同一个 MDL 锁
3. 在引擎层，认为这是不同的表，因此 MDL 锁之后的执行过程，会根据分区表规则，只访问必要的分区





## 43.4 分区表的应用场景



优点：

1. 对业务透明，相对于用户分表来说，使用分区表的业务代码更简洁
2. 很方便的清理历史数据



应用场景：

1. 游戏存放角色数据，根据uid分区
2. 统计流水，按照月分区



分区原则

1. 单表或者单分区的数据一千万行，只要没有特别大的索引，对于现在的硬件能力来说都已经是小表了
2. 分区也不要提前预留太多，在使用之前预先创建即可。比如，如果是按月分区，每年年底时再把下一年度的 12 个新分区创建上即可。对于没有数据的历史分区，要及时的 drop 掉



# 第四十四章 自增ID用完



主题：看看 MySQL 里面的几种自增 id，一起分析一下它们的值达到上限以后，会出现什么情况



## 44.1 表自增ID

```mysql
create table t(id int unsigned auto_increment primary key) auto_increment=4294967295;
insert into t values(null);

insert into t values(null);
#Duplicate entry '4294967295' for key 'PRIMARY'
```

表的自增 id 达到上限后，再申请时它的值就不会改变，进而导致继续插入数据时报主键冲突的错误



## 44.2 InnoDB 系统自增row_id

1. row_id 写入表中的值范围，是从 0 到 2^48-1
2. row_id 达到上线后，会归0，如果出现相同的row_id，后写的数据会覆盖之前的数据



## 44.3 Xid

MySQL 内部维护了一个全局变量 global_query_id，每次执行语句的时候将它赋值给 Query_id，然后给这个变量加 1。如果当前语句是这个事务执行的第一条语句，那么 MySQL 还会同时把 Query_id 赋值给这个事务的 Xid。

 global_query_id 定义的长度是 8 个字节，这个自增值的上限是 264-1。要出现这种情况，必须是下面这样的过程

1. 执行一个事务，假设 Xid 是 A
2. 接下来执行 264次查询语句，让 global_query_id 回到 A
3. 再启动一个事务，这个事务的 Xid 也是 A



## 44.4 InnoDB trx_id

InnoDB 数据可见性的核心思想是：每一行数据都记录了更新它的 trx_id，当一个事务读到一行数据的时候，判断这个数据是否可见的方法，就是通过事务的一致性视图与这行数据的 trx_id 做对比



nnoDB 内部维护了一个 max_trx_id 全局变量，每次需要申请一个新的 trx_id 时，就获得 max_trx_id 的当前值，然后并将 max_trx_id 加 1。max_trx_id 会持久化存储，重启也不会重置为 0，那么从理论上讲，只要一个 MySQL 服务跑得足够久，就可能出现 max_trx_id 达到 2^48-1 的上限，然后从 0 开始的情况。当达到这个状态后，MySQL 就会持续出现一个脏读的 bug。



## 44.5 thread_id

系统保存了一个全局变量 thread_id_counter，每新建一个连接，就将 thread_id_counter 赋值给这个新连接的线程变量。thread_id_counter 定义的大小是 4 个字节，因此达到 232-1 后，它就会重置为 0，然后继续增加





## 44.6 小结

1. 表的自增 id 达到上限后，再申请时它的值就不会改变，进而导致继续插入数据时报主键冲突的错误
2. row_id 达到上限后，则会归 0 再重新递增，如果出现相同的 row_id，后写的数据会覆盖之前的数据
3. Xid 只需要不在同一个 binlog 文件中出现重复值即可。虽然理论上会出现重复值，但是概率极小，可以忽略不计
4. InnoDB 的 max_trx_id 递增值每次 MySQL 重启都会被保存起来，所以我们文章中提到的脏读的例子就是一个必现的 bug，好在留给我们的时间还很充裕
5. thread_id 是我们使用中最常见的，而且也是处理得最好的一个自增 id 逻辑了





# 第四十五章 附录



## 45.1 术语

1. DDL（Data Definition Languages）语句：数据定义语言，这些语句定义了不同的数据段，[数据库](https://cloud.tencent.com/solution/database?from=10680)，表，列，索引等数据库对象。常用的语句关键字主要包括create,drop,alter等
2. DML（Data Manipulation Language）语句：数据操纵语句，用于添加，删除，更新和查询数据库记录，并检查数据完整性。常用的语句关键字主要包括insert，delete,update,select等
3. DCL（Data Control Language）语句：数据控制语句，用于控制不同数据段直接的许可和访问级别的语句。这些语句定义了数据库，表，字段，用户的访问权限和安全级别。主要的语句关键字包括grant,revoke等





## 45.2 临时表



创建表

```mysql
create temporary table temp_t(id int primary key, a int, b int, index(b))engine=innodb;
insert into temp_t select * from t2 where b>=1 and b<=2000;
select * from t1 join temp_t on (t1.b=temp_t.b);
```







