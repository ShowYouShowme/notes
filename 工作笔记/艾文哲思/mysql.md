# 第一章 安装

## 1.1 yum安装

1. mariadb

   ```shell
   # 不管是redis还是mysql或者gcc这种工具，尽量用yum安装，源码编译安装太麻烦！
   # 如果C++开发过程需要用到对应sdk，比如openssl-devel之类，也可以考虑用yum安装，编译安装太麻烦了，或者干脆更换编程语言！
   # centos7
   yum install -y mariadb-server
   
   #启动
   systemctl start mariadb
   
   #开机启动
   systemctl enable mariadb
   
   # 初始化
   mysql_secure_installation
   
   ## 
   0. 设置root密码(设置不设置都可以)  n
   1. 去除匿名用户 y
   2. 去除root远程登陆权限 y
   3. 删除test库 y
   4. 重新加载权限表 y
   ```

2. mysql

   ```shell
   #下载yum源
   wget https://dev.mysql.com/get/mysql80-community-release-el7-7.noarch.rpm
   
   #安装源
   yum localinstall mysql80-community-release-el7-7.noarch.rpm
   
   #安装工具
   sudo yum install -y yum-utils
   
   #查看所有的mysql
   yum repolist all | grep mysql
   
   #查看当前激活的mysql
   yum repolist enabled | grep "mysql.*-community.*"
   
   
   #启用指定版本的mysql
   yum-config-manager --disable mysql80-community
   yum-config-manager --enable mysql57-community
   
   #检查当前启用版本是否为5.7
   yum repolist enabled | grep mysql
   
   #安装mysql
   yum install -y mysql-community-server
   
   #启动服务
   systemctl  start mysqld
   
   #初始化设置
   
   ##获取初始密码
   grep 'temporary password' /var/log/mysqld.log
   
   
   ##初始化
   mysql_secure_installation
   
   ## 注意:新密码必须包含大写字母、小写字母、数字、标点符号，且密码长度至少为 8
   ## 这里会要求你输入初始密码
   0. 设置root密码(设置不设置都可以)  n
   1. 去除匿名用户 y
   2. 去除root远程登陆权限 y
   3. 删除test库 y
   4. 重新加载权限表 y
   
   
   
   #查看mysql的全部安装文件
   rpm -ql mysql-community-server | less
   ```

   



## 1.2 docker安装

```shell
docker pull mysql:5.7
```



# 第二章 常见操作



##  2.1 导出数据

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

   



## 2.2 导入数据

1. 创建数据库

   ```shell
   mysql -u${user} -p${passwd} -e "create database ${dbName}"
   
   mysql -uroot -proot@appinside -e "create database db_tars"
   ```

2. 执行sql脚本

   ```shell
   mysql -u${user} -p${passwd} ${dbName} < ${sqlFile}
   
   mysql -uroot -proot@appinside db_tars < db_tars.sql
   
   #也可以不指定DB
   mysql -uroot -ptars2015 < tables_xxl_job.sql
   ```

3. 删除数据库

   ```shell
   mysql -u${user} -p${passwd} -e "DROP DATABASE ${dbName}"
   ```





## 2.3 服务管理

1. 重启

   ```shell
   systemctl restart mariadb
   ```

2. 停止服务

   ```shell
   systemctl stop mariadb
   ```

3. 启动服务

   ```shell
   systemctl start mariadb
   ```

4. 查看服务状态

   ```shell
   systemctl status mariadb
   ```

5. 设置开机启动

   ```shell
   systemctl enable mariadb
   ```

   



## 2.3 锁

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



## 2.4 用户管理

1. 创建用户

   ```mysql
   >use mysql;
   
   >create user gitea identified by "123456";
   
   >flush privileges;
   ```

2. 配置账户权限

   ```mysql
   mysql > GRANT ALL PRIVILEGES ON *.* TO '${账号}'@'%' IDENTIFIED BY '${访问密码}' WITH GRANT OPTION;
   mysql > flush privileges;
   
   
   ## 限定账号tars只能在10.10.10.23上面登录
   grant all on *.* to 'tars'@'10.10.10.23' identified by 'tars2015';
   
   # 授予局域网172.31.31 里面的任何机器
   grant all on db_tars.* to 'tars'@'172.31.31.%' identified by 'tars2015';
   
   
   grant all on ${数据库}.${表} to "${用户名}"@"${IP}" identified by "${密码}";
   ```

3. 删除无密码用户

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

   



## 2.5 连接数

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
   
   # 杀死指定任务
   kill ${id};
   ```

4. 查看MySQL服务器状态

   ```shell
   show status;
   
   # Threads_connected  当前的连接数
   # Connections  试图连接到(不管是否成功)MySQL服务器的连接数。
   # Max_used_connections  服务器启动后已经同时使用的连接的最大数量。
   ```



## 2.6 登录

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
   
   





## 2.7 日志



### 2.7.1 日志类型

 1. 重做日志(redo log)

    ```
    InnoDB的事务日志
    ```

 2. 回滚日志(undo log)

    ```
    InnoDB的事务日志
    ```

 3. 二进制日志(binlog)

    ```
    记录DDL(数据定义语言)和DML(数据操作语言)语句并包含语句执行时间
    ```

 4. 错误日志(errorlog)

 5. 慢查询日志(slow query log)

 6. 一般查询日志(general log)

 7. 中继日志(relay log)

    ```
    MySQL通过binlog和relay log进行主从数据同步，binlog由主库产生，从库通过复制io线程拉取binlog，写入到relay log中，sql线程读取relay log中的事务信息，并进行应用！
    ```




### 2.7.2 日志路径

 1. general_log_file

 ```shell
 mysql> show variables like 'general_log_file';
 
 # /usr/local/mysql/data/localhost.log
 ```

 2. log_error

 ```shell
 mysql> show variables like 'log_error';
 
 # /usr/local/mysql/data/localhost.localdomain.err
 ```

 3. slow_query_log_file

 ```shell
 mysql> show variables like 'slow_query_log_file';
 
 # /usr/local/mysql/data/localhost-slow.log
 ```











## 2.8 数据类型

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

5. Length和decimals

   + 字段数据类型为CHAR,VARCHAR时Length指字符串的长度

   + 数据类型为TINYINT、SMALLINT、MEDIUMINT、INT和BIGINT时，Length指**显示宽度**，不用填写！

   + 小数

     + 浮点数

       ```shell
       #FLOAT 4 字节
       
       #DOUBLE 8 字节
       
       #定义浮点数时不用指定Length和decimals,否则无法迁移到其它数据库
       ```

     + 定点数

       ```shell
       #DECIMAL 用于存放精确的小数,定义时必须填写Length和decimals
       
       #定义
       #P是表示有效数字数的精度(即Length)，P范围为1〜65
       #D是表示小数点后的位数,范围是(0~30)
       column_name  DECIMAL(P,D);
       
       #例子
       amount DECIMAL(6,2);
       
       #amount的范围是-9999.99到9999.99
       ```

   + 数据库里使用小数的情况很少，只有字段为CHAR和VARCHAR时需要关注Length，decimals不用管！




## 2.9 统计

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



## 2.10 时区



### 2.10.1 查看时区

```shell
show variables like "%time_zone%";
```





### 2.10.2 设置时区

```shell
#配置文件路径/etc/my.cnf
[mysqld] 
default-time-zone='+08:00'
```





### 2.10.3 临时修改时区

```shell
set time_zone = '+8:00';
set global time_zone='+08:00';
```



### 2.10.4 时区转换函数

```shell
CONVERT_TZ
```





## 2.11 常用SQL语句




### 2.11.1 清空表

   ```mysql
   TRUNCATE TABLE tb_student_course;
   ```

### 2.11.2 查询

   ```mysql
   SELECT * FROM tb_student_course;
   ```

### 2.11.3 插入数据

   ```mysql
   INSERT INTO tb_courses \
             (course_id,course_name,course_grade,course_info) \
       	  VALUES(1,'Network',3,'Computer Network');
   ```

### 2.11.4 修改数据

   ```mysql
   UPDATE tb_courses_new \
       SET course_name='DB',course_grade=3.5 \
       WHERE course_id=2;
   ```

### 2.11.5 删除数据

   ```mysql
   -- 删除全部数据
   DELETE FROM tb_courses_new;
   
   -- 删除指定数据
   DELETE FROM tb_courses
       WHERE course_id=4;
   ```

### 2.11.6 创建表

   ```mysql
   CREATE TABLE tb_courses \
       ( \
       course_id INT NOT NULL AUTO_INCREMENT, \
       course_name CHAR(40) NOT NULL,\
       course_grade FLOAT NOT NULL,\
       course_info CHAR(100) NULL,\
       PRIMARY KEY(course_id)\
       );
   ```

### 2.11.7 创建数据库

   ```mysql
   CREATE DATABASE test_db;
   ```

### 2.11.8 查看数据库

   ```mysql
   SHOW DATABASES;
   ```

### 2.11.9 选择数据库

   ```mysql
   USE test_db;
   ```

   

### 2.11.10 查看表

```mysql
SHOW TABLES;
```

### 2.11.11 查看表结构

```mysql
DESC tb_courses;
```

### 2.11.12 查看表结构和注释

```mysql
select table_schema,table_name,column_name,column_type,column_key,is_nullable,column_default,column_comment,character_set_name

from information_schema.columns where table_schema='库名' and table_name='表名';
```

### 2.11.13 普通索引

```mysql
mysql> CREATE TABLE tb_stu_info
    -> (
    -> id INT NOT NULL,
    -> name CHAR(45) DEFAULT NULL,
    -> dept_id INT DEFAULT NULL,
    -> age INT DEFAULT NULL,
    -> height INT DEFAULT NULL,
    -> INDEX(height)
    -> );
```


​    

### 2.11.14 唯一索引

```mysql
mysql> CREATE TABLE tb_stu_info2
    -> (
    -> id INT NOT NULL,
    -> name CHAR(45) DEFAULT NULL,
    -> dept_id INT DEFAULT NULL,
    -> age INT DEFAULT NULL,
    -> height INT DEFAULT NULL,
    -> UNIQUE INDEX(height)
    -> );
```

### 2.11.15 约束

1. 主键约束

   ```mysql
       mysql> CREATE TABLE tb_emp3
           -> (
               -> id INT(11) PRIMARY KEY,
               -> name VARCHAR(25),
               -> deptId INT(11),
               -> salary FLOAT
               -> );
   ```

2. 外键约束

   ```mysql
       mysql> CREATE TABLE tb_dept1
           -> (
           -> id INT(11) PRIMARY KEY,
           -> name VARCHAR(22) NOT NULL,
           -> location VARCHAR(50)
           -> );
           
           
           mysql> CREATE TABLE tb_emp6
           -> (
           -> id INT(11) PRIMARY KEY,
           -> name VARCHAR(25),
           -> deptId INT(11),
           -> salary FLOAT,
           -> CONSTRAINT fk_emp_dept1
           -> FOREIGN KEY(deptId) REFERENCES tb_dept1(id)
           -> );
   ```

3. 唯一约束

   ```mysql
       mysql> CREATE TABLE tb_dept2
           -> (
           -> id INT(11) PRIMARY KEY,
           -> name VARCHAR(22) UNIQUE,
           -> location VARCHAR(50)
           -> );
   ```

4. 检查约束

   ```mysql
       mysql> CREATE TABLE tb_emp7
           -> (
           -> id INT(11) PRIMARY KEY,
           -> name VARCHAR(25),
           -> deptId INT(11),
           -> salary FLOAT,
           -> CHECK(salary>0 AND salary<100),
           -> FOREIGN KEY(deptId) REFERENCES tb_dept1(id)
           -> );
   ```

5. 非空约束

   ```mysql
       mysql> CREATE TABLE tb_dept4
           -> (
           -> id INT(11) PRIMARY KEY,
           -> name VARCHAR(22) NOT NULL,
           -> location VARCHAR(50)
           -> );
   ```

6. 默认值约束

   ```mysql
       mysql> CREATE TABLE tb_dept3
           -> (
           -> id INT(11) PRIMARY KEY,
           -> name VARCHAR(22),
           -> location VARCHAR(50) DEFAULT 'Beijing'
           -> );
   ```

   



### 2.11.16 查看默认引擎

```mysql
show engines \G;
```




## 2.12 压力测试



### 2.12.1 安装

```shell
yum -y install epel-release
yum -y install sysbench
```



### 2.12.2 压测

```shell
#创建数据库
create database sbtest;

#准备数据

sysbench --mysql-host=127.0.0.1 \
--mysql-port=3306 \
--mysql-user=root \
--mysql-password=tars2015 \
/usr/share/sysbench/oltp_common.lua \
--tables=10 \
--table_size=100000 \
prepare


#测试一:测试读写性能
#测试
sysbench --threads=4 \
--time=20 \
 --report-interval=5 \
 --mysql-host=127.0.0.1 \
--mysql-port=3306 \
--mysql-user=root \
--mysql-password=tars2015 \
/usr/share/sysbench/oltp_read_write.lua \
--tables=10 \
 --table_size=100000 \
run


#测试二：测试只读的性能
sysbench --threads=4 \
--time=20 \
 --report-interval=5 \
 --mysql-host=127.0.0.1 \
--mysql-port=3306 \
--mysql-user=root \
--mysql-password=tars2015 \
/usr/share/sysbench/oltp_read_only.lua \
--tables=10 \
 --table_size=100000 \
run


#测试三:测试只写的性能
sysbench --threads=4 \
--time=20 \
 --report-interval=5 \
 --mysql-host=127.0.0.1 \
--mysql-port=3306 \
--mysql-user=root \
--mysql-password=tars2015 \
/usr/share/sysbench/oltp_write_only.lua \
--tables=10 \
 --table_size=100000 \
run
```



```shell
#io性能压测

#创建文件
sysbench fileio --file-num=5 --file-total-size=2G prepare

#运行
sysbench --events=5000 \
--threads=16 \
fileio \
--file-num=5 \
--file-total-size=2G \
--file-test-mode=rndrw \
--file-fsync-freq=0 \
--file-block-size=16384 \
run
```



```shell
#CPU性能测试
sysbench cpu --threads=40 --events=10000 --cpu-max-prime=20000 run
```







# 第三章 附录


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
