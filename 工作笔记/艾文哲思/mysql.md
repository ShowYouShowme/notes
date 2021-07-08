#  导出数据

1. 只导出表结构

   ```shell
   mysqldump   --opt -d  ${dbName}  -u${user}  -p${passwd} > ${outFile}
   
   mysqldump   --opt -d  hp_activity  -uroot  -proot@appinside  >hp_activity.sql
   ```

2. 只导出数据

   ```shell
   mysqldump   -t  ${dbName}    -u${user}  -p${passwd}  > ${outFile}
   
   mysqldump   -t  hp_activity    -uroot  -proot@appinside  >   hp_activity_data.sql
   ```

3. 同时导出表结构和数据

   ```shell
   mysqldump   ${dbName}    -u${user}  -p${passwd}  > ${outFile}
   
   mysqldump   hp_activity    -uroot  -proot@appinside  >   hp_activity_all.sql
   ```
   
4. 导出所有的库

   ```shell
   mysqldump -u${user} -p${passwd} --all-databases > all.sql
   ```

   





# 导入数据

1. 创建数据库

   ```shell
   mysql -u${user} -p${passwd} -e "create database ${dbName}"
   
   mysql -uroot -proot@appinside -e "create database db_tars"
   ```

2. 执行sql脚本

   ```shell
   mysql -u${user} -p${passwd} ${dbName} < ${sqlFile}
   
   mysql -uroot -proot@appinside db_tars < db_tars.sql
   ```

3. 删除数据库

   ```shell
   mysql -u${user} -p${passwd} -e "DROP DATABASE ${dbName}"
   ```




# 增加字段

> 用Navicat Premium增加字段，提示Incorrect column name 'aa' 的原因:字段里面包含空格





# 常用命令

1. 重启

   ```shell
   # 第一种方法
   service mysqld restart 
   
   # 第二种方法
   /etc/init.d/mysql restart
   ```

2. 登录

   ```shell
   /usr/local/mysql-5.6.26/bin/mysql -uroot -p
   ```

3. 停止服务

   ```shell
   service mysqld stop
   ```

4. 启动服务

   ```shell
   service mysqld start
   ```

   



# 删除没有密码的用户

```shell
use mysql;
# 查看用户的权限
select host,user,password from user; # 5.6版本

select user,authentication_string,host from user; # 5.7版本

drop user 'zhangsan'@'%';

drop user '${user}'@'${host}';

# 没有名称的用户
drop user ' '@'%';

# 刷新权限
flush  privileges;

# 赋予权限
grant all on *.* to 'tars'@'%' identified by 'tars2015' with grant option;
```



# 数据库连接数太多







# 锁

1. **写锁[排他锁]**

   ```sql
   lock tables test write;
   ```

   其它会话读/写表`test`会阻塞，也无法获取表`test`的read或write锁。持有锁的会话可以读/写表！

2. **读锁[共享锁]**

   ```sql
   lock tables test read;
   ```

   该会话和其它会话只能读，不能往表里写入数据。其它会话可以获取read锁！



# 配置账户权限

```shell
mysql > GRANT ALL PRIVILEGES ON *.* TO '${账号}'@'%' IDENTIFIED BY '${访问密码}' WITH GRANT OPTION;
mysql > flush privileges;


## 限定账号tars只能在10.10.10.23上面登录
grant all on *.* to 'tars'@'10.10.10.23' identified by 'tars2015';

# 授予局域网172.31.31 里面的任何机器
grant all on db_tars.* to 'tars'@'172.31.31.%' identified by 'tars2015';


grant all on ${数据库}.${表} to "${用户名}"@"${IP}" identified by "${密码}";
```



# 连接数

1. 查看配置的最大连接数

   ```mysql
   show variables like '%max_connections%';
   ```

2. 配置最大连接数

   ```shell
   # 在配置文件my.cnf里增加
   max_connections=2048
   # 重启mysql
   service mysql restart
   ```

3. 显示正在执行的MySQL连接

   ```shell
   show  processlist;
   ```

4. 查看MySQL服务器状态

   ```shell
   show status;
   
   # Threads_connected  当前的连接数
   # Connections  试图连接到(不管是否成功)MySQL服务器的连接数。
   # Max_used_connections  服务器启动后已经同时使用的连接的最大数量。
   ```



# 登录

1. 登录命令

   ```shell
   # 登录命令
   mysql -h ${IP} -P ${PORT} -u ${ACCOUNT} -p
   mysql -h 127.0.0.1 -P 4406 -u tars -p
   ```

2. localhost和127.0.0.1的区别

   ```shell
   # 采用TCP的方式连接
   mysql -h 127.0.0.1 -P 4406 -u tars -p
   
   # 采用unix domain socket连接
   mysql -h localhost -P 4406 -u tars -p
   # 上个命令等价于
   mysql -P 4406 -u tars -p
   
   # 常见错误 : 文件/tmp/mysql.sock 在unix domain socket连接时使用,用TCP连接即可
   # Can't connect to local MySQL server through socket '/tmp/mysql.sock'
   
   # 查看账号权限时,同时存在localhost和127.0.0.1,次二者不一样
   ```
   
   





# 日志

## 1 日志类型

> 1. 重做日志(redo log)
>
>    ```
>    InnoDB的事务日志
>    ```
>
> 2. 回滚日志(undo log)
>
>    ```
>    InnoDB的事务日志
>    ```
>
> 3. 二进制日志(binlog)
>
>    ```
>    记录DDL(数据定义语言)和DML(数据操作语言)语句并包含语句执行时间
>    ```
>
> 4. 错误日志(errorlog)
>
> 5. 慢查询日志(slow query log)
>
> 6. 一般查询日志(general log)
>
> 7. 中继日志(relay log)
>
>    ```
>    MySQL通过binlog和relay log进行主从数据同步，binlog由主库产生，从库通过复制io线程拉取binlog，写入到relay log中，sql线程读取relay log中的事务信息，并进行应用！
>    ```
>
>    



## 2 查看日志路径

> 1. general_log_file
>
> ```shell
> mysql> show variables like 'general_log_file';
> 
> # /usr/local/mysql/data/localhost.log
> ```
>
> 2. log_error
>
> ```shell
> mysql> show variables like 'log_error';
> 
> # /usr/local/mysql/data/localhost.localdomain.err
> ```
>
> 3. slow_query_log_file
>
> ```shell
> mysql> show variables like 'slow_query_log_file';
> 
> # /usr/local/mysql/data/localhost-slow.log
> ```





# Length和decimals

+ 细节

  1. 字段数据类型为CHAR,VARCHAR时Length指字符串的长度

  2. 数据类型为TINYINT、SMALLINT、MEDIUMINT、INT和BIGINT时，Length指**显示宽度**，不用填写！

  3. 小数

     + 浮点数

       ```shell
       # FLOAT 4 字节
       
       # DOUBLE 8 字节
       
       # 定义浮点数时不用指定Length和decimals,否则无法迁移到其它数据库
       ```

     + 定点数

       ```shell
       
       # DECIMAL 用于存放精确的小数,定义时必须填写Length和decimals
       
       # 定义
       # P是表示有效数字数的精度(即Length)，P范围为1〜65
       # D是表示小数点后的位数,范围是(0~30)
       column_name  DECIMAL(P,D);
       
       # 例子
       amount DECIMAL(6,2);
       
       # amount的范围是-9999.99到9999.99
       ```

       

+ 总结

  > 数据库里使用小数的情况很少，只有字段为CHAR和VARCHAR时需要关注Length，decimals不用管！





# 数据类型

1. 日期和时间类型

   ```shell
   YEAR                                  1 字节,年份,比如"2019"
   TIME                                  3 个字节,时间"23:59:25"
   DATE                                  3 个字节,日期"1949-10-01"
   DATETIME                              8 个字节,日期和时间"1949-10-01 11:11:11" 用NOW()输入当前日期和时间
   TIMESTAMP                             4 个字节,日期和时间"1949-10-01 11:11:11" 用CURRENT_TIMESTAMP 输入当前日期和时间
   ```

2. 字符串类型

   ```shell
   # CHAR 和 VARCHAR
   CHAR(M)						固定长度为M
   VARCHAR(M)				可变长度，字符串长度最大为M
   
   # TEXT类型
   TINYTEXT          L+1 字节, 在此L< 2^8 	-	1
   TEXT              L+2 字节, 在此L< 2^16 - 1
   MEDIUMTEXT        L+3 字节, 在此L< 2^24 - 1
   LONGTEXT          L+4 字节, 在此L< 2^32 - 1
   
   # ENUM类型
   枚举类型，值只能是几个字符串的一个
   ${field} ENUM('v1', 'v2', ..., 'vn')
   # SET类型
   集合类型，值只能是几个字符串中的若干个
   ${field} SET('v1', 'v2', ..., 'vn')
   ```

3. 数字类型

   + 整数类型

     ```shell
     TINYINT                               1 字节 
     SMALLINT                              2 个字节 
     MEDIUMINT                             3 个字节 
     INT                                   4 个字节 
     INTEGER                               4 个字节 
     BIGINT                                8 个字节 
     
     # 定义时设置显示宽度(鸡肋的功能)
     int(11)
     
     # 定义时设置为无符号整数
     unsigned
     ```

   + 小数

     ```shell
     # 浮点类型
     FLOAT                                 4 个字节 
     DOUBLE                                8 个字节
     
     # 定点类型
     # M:长度 D:小数位数
     DECIMAL(M,D)                          M字节(D+2 , 如果M < D) 
     ```

4. 二进制类型

   ```shell
   BINARY(M)														字节数为M，允许0～M的定长二进制数据
   VARBINARY(M)												字节数为实际数据长度+1，允许0～M的定长二进制数据
   BIT(M)															M位二进制数据，M最大值为64
   TINYBLOB														可变长二进制，最多2^8-1个字节
   BLOB 																可变长二进制，最多2^16-1个字节
   MEDIUMBLOB													可变长二进制，最多2^24-1个字节
   LONGBLOB 														可变长二进制，最多2^32-1个字节
   ```

   




# mysql 客户端

***



## phpmysqladmin

***

```shell
# 使用docker安装 登录界面使用mysql的账号和密码登录
docker run --name myadmin -d -e PMA_HOST=178.128.61.189 -e PMA_PORT=8306 -p 8080:80 phpmyadmin/phpmyadmin:5.0.2


docker run --name myadmin -d -e PMA_HOST=${mysqlHost} -e PMA_PORT=${mysqlPort} -p 8080:80 phpmyadmin/phpmyadmin:5.0.2
```





## navicat

***

```shell
mac 上面使用有bug

# 防止自动断开
编辑链接 --> 高级 --> 保持连接间隔 --> 30s
```





## mysql-clinet

***

```shell
mysql 自带的客户端
```





## Mycli

***

```shell
自带补全功能
```



# 常见命令

***

1. 显示正在运行的线程[会话session]

   ```shell
   show processlist;
   ```

2. 杀死某个线程

   ```shell
   kill ${线程id}
   ```





# 常见问题

***

1. Waiting for table metadata lock：后续对该表任何操作都会阻塞

   + 原因一：存在未提交的事务

     ```python
     # 查找未提交的事务的线程id
     select * from information_schema.innodb_trx\G;
     
                         trx_id: 303835
                      trx_state: RUNNING
                    trx_started: 2020-08-05 13:18:24
          trx_requested_lock_id: NULL
               trx_wait_started: NULL
                     trx_weight: 2
            trx_mysql_thread_id: 24   # 这个就是未提交事务的线程ID
                      trx_query: NULL
            trx_operation_state: NULL
              trx_tables_in_use: 0
              trx_tables_locked: 0
               trx_lock_structs: 1
          trx_lock_memory_bytes: 360
                trx_rows_locked: 0
              trx_rows_modified: 1
        trx_concurrency_tickets: 0
            trx_isolation_level: REPEATABLE READ
              trx_unique_checks: 1
         trx_foreign_key_checks: 1
     trx_last_foreign_key_error: NULL
      trx_adaptive_hash_latched: 0
      trx_adaptive_hash_timeout: 10000
               trx_is_read_only: 0
     trx_autocommit_non_locking: 0
         
     # 杀死线程
     kill 24
     ```

2. 长事物运行，阻塞DDL，继而阻塞所有同表的后续操作

   ```shell
   kill 掉 DDL所在的session
   ```

3. 在一个显式的事务中，对TableA进行了一个失败的操作（比如查询了一个不存在的字段），这时事务没有开始，但是失败语句获取到的锁依然有效，没有释放performance_schema.events_statements_current表中可以查到失败的语句

   ```shell
   performance_schema.events_statements_current找到其sid, kill 掉该session. 也可以 kill 掉DDL所在的session
   ```




# 统计相关

```mysql
# 获取当前日期和时间
SELECT NOW();

SELECT CURDATE(); # 获取当前日期

SELECT CURTIME(); # 返回当前时间

SELECT * FROM plot_statistics WHERE DATE(log_time) = "2021-07-07";  # 统计某一天


SELECT * FROM plot_statistics WHERE DATE(log_time) = CURDATE();  # 统计当天

select * from plot_statistics where date(log_time) = date_sub(CURDATE()  ,interval 1 day); # 统计前一天


select * from plot_statistics where TO_DAYS(NOW()) - TO_DAYS(log_time) <= 1; # 统计昨天和今天的
```

