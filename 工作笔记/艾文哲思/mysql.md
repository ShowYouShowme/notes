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
   0. Enter current password for root  直接按下回车
   1. 设置root密码(设置不设置都可以)  n
   2. 去除匿名用户 y
   3. 去除root远程登陆权限 y
   4. 删除test库 y
   5. 重新加载权限表 y
   
   ## 登录
   mysql -uroot -p   直接回车,没有密码
   ```

2. mysql：版本是5.7.44，注意docker安装的要和这个版本一样

   ```shell
   #下载yum源
   wget https://dev.mysql.com/get/mysql80-community-release-el7-7.noarch.rpm
   
   #安装源
   yum localinstall mysql80-community-release-el7-7.noarch.rpm -y
   
   #安装工具
   yum install -y yum-utils
   
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



## 1.3 启动命令

1. 使用systemctl

   ```shell
   systemctl start mysqld
   ```

2. 使用mysqld启动，可以配合pm2进行管理

   ```shell
   # 精灵模式
   mysqld --defaults-file=/etc/my.cnf --daemonize --user=mysql
   
   # 前台启动, 配合PM2管理即可,方便监控
   mysqld --defaults-file=/etc/my.cnf --user=mysql
   
   #PM2的配置文件
   module.exports = {
     apps : [{
       "name"       : "mysqld",
       "script"     : "/usr/sbin/mysqld",
       "exec_interpreter": "none",
       "exec_mode"  : "fork_mode",
       "args"       : "--defaults-file=/etc/my.cnf --user=mysql"
     }]
   };
   ```



## 1.4 关闭Mysql

1. 使用systemctl

   ```shell
   systemctl stop mysqld
   ```

2. 使用mysql客户端关闭

   ```shell
   mysql客户端连上后; 执行shutdown 命令
   ```

3. kill命令：不推荐

   ```shell
   kill -9 ${pid}
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
   mysql -uroot -p'tars2015' < tables_xxl_job.sql
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
   
   
   # 允许从任何机器登录
   grant all on *.* to 'tars'@'%' identified by 'tars2015';
   
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

4. 白名单配置MySQL5.7

   ```ini
   [step-1]
   desc = 登录
   cmd = mysql -uroot -pmysql
   
   [step-2]
   desc = 切换至mysql库
   cmd = use mysql;
   
   [step-3]
   desc = 查看有白名单权限的用户
   cmd = select Host,User from user;
   
   [step-4]
   desc = 指定ip有权限访问mysql
   cmd = GRANT ALL ON *.* to root@'192.168.1.4' IDENTIFIED BY 'your-root-password';
   #如果无密码
   cmd = GRANT ALL ON *.* to root@'192.168.1.4' ;
   
   ;允许一个网段登录
   cmd = GRANT ALL PRIVILEGES ON *.* TO root@'192.168.192.%' IDENTIFIED BY 'root' WITH GRANT OPTION;
   
   ;或者
   cmd = GRANT ALL PRIVILEGES ON *.* TO root@'192.168.%.%' IDENTIFIED BY 'root' WITH GRANT OPTION;
   
   [step-5]
   desc = 删除白名单用户的权限
   cmd = DELETE FROM user WHERE User='username' and Host='host';
   
   [step-6]
   desc = 刷新权限
   cmd = FLUSH PRIVILEGES;
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
   
   #command列: Sleep 空闲链接
   
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
   
   #如果密码有特殊字符
   mysql -uroot -p'tars2015'
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
   
   
   在创建时间字段的时候
   
   DEFAULT CURRENT_TIMESTAMP
   表示当插入数据的时候，该字段默认值为当前时间
   
   ON UPDATE CURRENT_TIMESTAMP
   表示每次更新这条数据的时候，该字段都会更新成当前时间
   
   
   CREATE TABLE `mytest` (
       `text` varchar(255) DEFAULT '' COMMENT '内容',
       `create_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
       `update_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间'
   ) ENGINE=InnoDB DEFAULT CHARSET=utf8;
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

   + DATETIME：默认显示长度为19个字符，设置为0即可

     ```
     Length = 8
     8个字符显示,精确到秒
     
     Length = 14
     14个字符显示,精确到秒
     
     Length = 17
     17个字符显示,精确到毫秒
     
     Length = 19
     19个字符显示,精确到秒
     ```
   
     
   
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

# 获取当前时间戳,秒为单位
SELECT UNIX_TIMESTAMP();


# 日期格式转换

## 日期 时间
select DATE_FORMAT(NOW(), '%Y-%m-%d %H:%i:%s');
## 日期
select DATE_FORMAT(NOW(), '%Y-%m-%d');
## 时间
select DATE_FORMAT(NOW(), '%H:%i:%s');


# 时间转化为秒数
select TIME_TO_SEC(NOW());
select TIME_TO_SEC('2024-03-07 23:45:20');
select SEC_TO_TIME(85520);


# 日期加减法 --统计必备

## 日期时间戳加减
select NOW();    -- 2024-03-07 23:41:47
select DATE_SUB(NOW(),interval 1 year); -- 2023-03-07 23:41:47
select DATE_SUB(NOW(),interval 1 quarter); -- 2023-12-07 23:41:47
select DATE_SUB(NOW(),interval 1 month); -- 2024-02-07 23:41:47
select DATE_SUB(NOW(),interval 1 week); -- 2024-02-29 23:41:47
select DATE_SUB(NOW(),interval 1 day); -- 2024-03-06 23:41:47
select DATE_SUB(NOW(),interval 1 hour); -- 2024-03-07 22:41:47
select DATE_SUB(NOW(),interval 1 minute); -- 2024-03-07 23:40:47
select DATE_SUB(NOW(),interval 1 second); -- 2024-03-07 23:41:46
select DATE_SUB(NOW(),interval -1 day); -- 2024-03-08 23:41:47


select NOW();  -- 2024-03-07 23:39:14
select DATE_ADD(NOW(),interval 1 year); -- 2025-03-07 23:39:14
select DATE_ADD(NOW(),interval 1 quarter); -- 2024-06-07 23:39:14
select DATE_ADD(NOW(),interval 1 month); -- 2024-04-07 23:39:14
select DATE_ADD(NOW(),interval 1 week); -- 2024-03-14 23:39:14
select DATE_ADD(NOW(),interval 1 day); -- 2024-03-08 23:39:14
select DATE_ADD(NOW(),interval 1 hour); -- 2024-03-08 00:39:14
select DATE_ADD(NOW(),interval 1 minute); -- 2024-03-07 23:40:14
select DATE_ADD(NOW(),interval 1 second); -- 2024-03-07 23:39:15
select DATE_ADD(NOW(),interval -1 day); -- 2024-03-06 23:39:14


## 日期加减
select CURDATE();    -- 2024-08-27
select DATE_SUB(CURDATE(),interval 1 year); -- 2023-08-27
select DATE_SUB(CURDATE(),interval 1 quarter); -- 
select DATE_SUB(CURDATE(),interval 1 month); -- 
select DATE_SUB(CURDATE(),interval 1 week); -- 
select DATE_SUB(CURDATE(),interval 1 day); -- 2024-08-26
select DATE_SUB(CURDATE(),interval 1 hour); -- 
select DATE_SUB(CURDATE(),interval 1 minute); -- 
select DATE_SUB(CURDATE(),interval 1 second); --
select DATE_SUB(CURDATE(),interval -1 day); -- 

select CURDATE();  -- 
select DATE_ADD(CURDATE(),interval 1 year); -- 
select DATE_ADD(CURDATE(),interval 1 quarter); -- 
select DATE_ADD(CURDATE(),interval 1 month); -- 
select DATE_ADD(CURDATE(),interval 1 week); -- 
select DATE_ADD(CURDATE(),interval 1 day); -- 
select DATE_ADD(CURDATE(),interval 1 hour); -- 
select DATE_ADD(CURDATE(),interval 1 minute); -- 
select DATE_ADD(CURDATE(),interval 1 second); -- 
select DATE_ADD(CURDATE(),interval -1 day); -- 


# 统计入库时,一般会记录create_at(时间戳),create_date(日期)管理后台请求接口时传入日期;利用MySQL将日期转换为时间戳;
# 利用条件WHERE from > t1 ADN to < t2 即可查出全部记录
# 日期时间戳转换
-- 将日期转为时间戳
select UNIX_TIMESTAMP(); -- 1709827653(获取当前时间戳)
select UNIX_TIMESTAMP('2024-03-08'); -- 1709827200(具体日期转为时间戳)
select UNIX_TIMESTAMP('2022-03-08 00:26:30'); -- 1646670390(具体时间日期转为时间戳)
-- 将时间戳转为具体时间
select FROM_UNIXTIME(1646670390); -- 2022-03-08 00:26:30(时间戳转化成日期)
select FROM_UNIXTIME(1646670390, '%y-%m-%d %H:%i:%s'); -- 22-03-08 00:26:30(时间戳转化成指定格式日期)
```



## 2.10 时区



### 2.10.1 查看时区

```shell
show variables like "%time_zone%";

// 查看当前时间
select now();

mysql> select now();
+---------------------+
| now()               |
+---------------------+
| 2024-08-23 09:07:43 |
+---------------------+
1 row in set (0.00 sec)
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
   #方法一
   INSERT INTO tb_courses \
             (course_id,course_name,course_grade,course_info) \
       	  VALUES(1,'Network',3,'Computer Network');
       	  
   #方法二
   INSERT INTO student VALUES(null, '张三丰', 28,4);
   
   #自增长或者有默认值的列,用方法一插入,直接忽略对应列
   #有默认值且限定为非NULL的列,不能插入NULL,会报错
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
   #创建临时表  
   create temporary table temp_t(id int primary key, a int, b int, index (b))engine=memory;
   ```

### 2.11.7 创建数据库

   ```mysql
   CREATE DATABASE test_db;
   
   #创建数据库时指定编码
   #utf8最多只能支持3bytes长度的字符编码，对于一些需要占据4bytes的文字，mysql的utf8就不支持了，要使用utf8mb4才行
   #utf8mb4_general_ci:排序规则,来用排序VARCHAR,CHAR,TEXT类型
    CREATE DATABASE `test2` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
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

索引字段是varchar时，必须要指定长度(navicat子部分填长度)

date 为varchar，最大长度255

KEY `date` (`date`(32)) USING BTREE

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



### 2.11.17 查看索引

```mysql
show index from tuser \G;
```



### 2.11.18 增加索引

```mysql
#语法
alter table ${tb_name} add index(${col_name});

alter table tuser add index(name);
```



### 2.11.19 事务

```mysql
#START TRANSACTION是在第一条select执行完后，才得到事务的一致性快照。而START TRANSACTION with consistent snapshot则是立即得到事务的一致性快照。

#启动事务
begin 或 start transaction 或者 start transaction with consistent snapshot;

#提交事务
commit

#事务回滚
rollback
```



### 2.11.20 删除数据库

```mysql
drop database test;
```



### 2.11.21 explain

```ini
[possible_keys]
desc = 可能使用的索引

[key]
desc = 实际使用的索引,如果没事使用索引,值是NULL

[Extra]
desc = 额外信息

Using filesort  = 需要排序
Using temporary = 使用临时表
Using index = 直接访问索引就足够获取到所需要的数据，不需要通过索引回表
Using index condition = 索引下压,部分where条件在Innodb引擎层判断,满足的记录才发送到server层,等价于 using index + 回表 + where 过滤
Using where = 优化器需要通过索引回表查询数据
```



### 2.11.22 SQL_MODE

查看

```shell
select @@GLOBAL.sql_mode
```



设置[关闭ONLY_FULL_GROUP，方便写统计业务]

```shell
[mysqld]
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
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



## 2.13 查看变量值

```shell
#transaction_isolation 是配置
show variables like 'transaction_isolation';

#或者
select @@secure_file_priv;
```





## 2.14 乱码配置

1. 配置

   ```ini
   [mysqld]
   character_set_server=utf8
   collation-server=utf8_general_ci
   skip-character-set-client-handshake
   #init_connect='SET NAMES utf8'
   #[client]
   #default-character-set=utf8
   ```

   

2. 查看编码

   ```mysql
   mysql> show variables like '%char%';
   ```

3. docker 里面的MySQL终端无法输入中文

   ```shell
   #先设置shell环境变量，再链接即可
   export LANG=en_US.UTF-8
   ```




## 2.15 字符集

myslq 可以设置数据库级别，表级别，列级别 字符集编码；

**优先级顺序为：数据库字符集 < 表字符集 < 列字符集；**

也就是 上面三个级别 字符集不一致时，以 更小范围的配置为准；

例如：数据库字符集为utf8 表字符集不设置的情况下 会默认 utf8 ，如果表主动设置了编码 utf8mb4;那么表的字符集编码就为utf8MB4;



### 2.15.1 创建库时指定编码

```sql
-- 创建数据库时,设置数据库的编码方式 
-- CHARACTER SET:指定数据库采用的字符集,utf8不能写成utf-8
-- COLLATE:指定数据库字符集的排序规则,utf8的默认排序规则为utf8_general_ci（通过show character set查看）
drop database if EXISTS dbtest;
create database dbtest CHARACTER SET utf8 COLLATE utf8_general_ci;
```



### 2.15.2 修改数据库编码

```sql
-- 修改数据库编码
alter database dbtest CHARACTER SET GBK COLLATE gbk_chinese_ci;
alter database dbtest CHARACTER SET utf8 COLLATE utf8_general_ci;
```





### 2.15.3 创建表时指定编码

```sql
-- 创建表时，设置表、字段编码
use dbtest;
drop table if exists tbtest;
create table tbtest(
id int(10) auto_increment,
user_name varchar(60) CHARACTER SET GBK COLLATE gbk_chinese_ci,
email varchar(60),
PRIMARY key(id)
)CHARACTER SET utf8 COLLATE utf8_general_ci;
```



### 2.15.4 修改表编码

```sql
-- 修改表编码
alter table tbtest character set utf8 COLLATE utf8_general_ci;
-- 修改字段编码
ALTER TABLE tbtest MODIFY email VARCHAR(60) CHARACTER SET utf8 COLLATE utf8_general_ci;
```



### 2.15.5 查看数据库编码

```sql
-- 查看创建数据库的指令并查看数据库使用的编码
show create database dbtest;
```



### 2.15.6 查看表编码

```sql
show create table t;
```





## 2.16 kill



### 2.16.1 kill query + 线程id

终止正在执行的语句，但是连接不断开。



### 2.16.2 kill connection +线程id

其中， connection可以省略。终止正在执行的语句，然后断开连接。







## 2.17 版本查看

1. 命令行客户端登录后信息包含版本

   ```shell
   mysql -uroot -p'tars2015'
   
   mysql: [Warning] Using a password on the command line interface can be insecure.
   Welcome to the MySQL monitor.  Commands end with ; or \g.
   Your MySQL connection id is 30
   Server version: 5.7.39 MySQL Community Server (GPL)
   
   Copyright (c) 2000, 2022, Oracle and/or its affiliates.
   
   Oracle is a registered trademark of Oracle Corporation and/or its
   affiliates. Other names may be trademarks of their respective
   owners.
   
   Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.
   ```

2. 使用status命令

   ```mysql
   mysql> STATUS
   ```

3. 使用sql语句

   ```sql
   select version();
   ```



## 2.18 存储过程



### 2.18.1 查看全部存储过程

```sql
select `name` from mysql.proc where db = '${your_db_name}' and `type` = 'PROCEDURE';

#例子
select `name` from mysql.proc where db = 'test' and `type` = 'PROCEDURE';

#或者
show procedure status \G;
```



### 2.18.2 查看存储过程创建代码

```sql
show create procedure proc_name;
show create function func_name;
```





### 2.18.3 删除存储过程

```sql
DROP PROCEDURE [ IF EXISTS ] <过程名>
```





# 第三章  差异对比

使用mysqldbcompare来对比两个数据库的差异



## 3.1 安装

url = https://dev.mysql.com/doc/connector-python/en/connector-python-versions.html

数据库版本：5.7, 5.6, 5.5

python版本： 3.5, 3.4, 2.7, 2.6

```shell
wget https://cdn.mysql.com/archives/mysql-connector-python-2.0/mysql-connector-python-2.0.5-1.el7.noarch.rpm

wget https://cdn.mysql.com/archives/mysql-utilities/mysql-utilities-1.6.5-1.el7.noarch.rpm

yum localinstall -y mysql-connector-python-2.0.5-1.el7.noarch.rpm
yum localinstall mysql-utilities-1.6.5-1.el7.noarch.rpm -y
```



## 3.2 对比差异

1. 创建数据库

   ```shell
   # 查看线上环境创建库的命令
   show create database rummy;
   
   # 在本地创建库
   CREATE DATABASE `rummy` DEFAULT CHARACTER SET utf8mb4
   
   # 用navicat 导入sql文件创建表; navicat 只需要导出线上数据库的表结构,不需要数据
   ```

2. 对比

   ```shell
   # test 是线上数据库, rummy是开发环境;这样可以得到线上数据库 变成 rummy需要的sql语句
   mysqldbcompare --server1=root:tars2015@192.168.1.49 --skip-row-count --skip-data-check --skip-table-options --server2=root:tars2015@192.168.1.49 test:rummy --changes-for=server1 --run-all-test --difftype=sql >> diff.txt
   
   --skip-data-check：跳过数据一致性验证
   --skip-row-count：跳过行数检查
   --skip-table-options：跳过CREATE语句() 外面的部分, 比如ENGINE=InnoDB AUTO_INCREMENT=363 DEFAULT CHARSET=utf8mb4 ROW_FORMAT=COMPACT
   -run-all-tests：运行完整比较，遇到第一次差异时不停止
   --changes-for=: 比较的基准,值为server1 或者 server2 默认是server1
   --difftype=DIFFTYPE：差异的信息显示的方式，有[unified|context|differ|sql]，默认是unified。如果使用sql，那么就直接生成差异的SQL，这样非常方便
   ```

3. 查找差异

   ```shell
   用notepad++ 查找 字符 ALTER 即可
   ```

4. 对比结果

   ```ini
   [有差异]
   desc = Database consistency check failed
   
   [相同]
   desc = Databases are consistent given skip options specified
   
   ; 表rm_player_career 在 test1 但不在test2
   WARNING: Objects in server1.test1 but not in server1.test2
   	TABLE: rm_player_career
   	
   ; 字段不一样
   ALTER TABLE `test1`.`rm_player_flow` 
     CHANGE COLUMN scene scene bigint(11) unsigned NOT NULL DEFAULT '0' COMMENT '场景类型', 
     CHANGE COLUMN channel channel float(11,0) unsigned NOT NULL DEFAULT '0' COMMENT '最新渠道id';
   ```

   

5. 对比的Makefile

   ```makefile
   prod:exportProd compare
   stage:exportStage compare
   exportProd:
   	rm -f backup.sql;
   	mysqldump -P 2000 -h192.168.1.115 -u root -p"yourPassword" --opt -d rummy > backup.sql
   
   exportStage:
   	rm -f backup.sql;
   	mysqldump -P 2500 -h192.168.1.115 -u tars -p"yourPassword"  --opt -d rummy > backup.sql
   deleteTest:
   	mysql -h 192.168.1.49 -uroot -p"tars2015" -e "drop database test"
   
   createTest:
   	mysql -h 192.168.1.49 -uroot -p"tars2015" -e "CREATE DATABASE test DEFAULT CHARACTER SET utf8mb4"
   
   import:
   	mysql -h 192.168.1.49 -uroot -p"tars2015" test < backup.sql
   
   compare:deleteTest createTest import
   	mysqldbcompare --server1=root:tars2015@192.168.1.49 --skip-row-count --skip-data-check --skip-table-options --server2=root:tars2015@192.168.1.49 test:rummy --changes-for=server1 --run-all-test --difftype=sql
   ```

   



## 3.3 使用navicat对比

点击工具--结构同步，源选择开发环境数据库，目标选择测试环境或者正式环境数据库，然后对比就可以了



# 第四章 慢查询

开启慢查询日志来进行性能优化

```ini
[配置项]
slow_query_log = 是否开启慢查询日志，1表示开启，0表示关闭

slow-query-log-file = MySQL数据库慢查询日志存储路径。可以不设置该参数，系统则会默认给一个缺省的文件host_name-slow.log

long_query_time = 慢查询阈值，当查询时间多于设定的阈值时，记录日志,单位是秒

min_examined_row_limit = 查询扫描过的最少记录数。这个变量和查询执行时间，共同组成了判别一个查询是否是慢查询的条件

log_queries_not_using_indexes = 未使用索引的查询也被记录到慢查询日志中

log_output = 日志存储方式。log_output='FILE'表示将日志存入文件，默认值是'FILE'。log_output='TABLE'表示将日志存入数据库

log_throttle_queries_not_using_indexes = 限制每分钟写入慢日志中的不走索引的SQL语句个数，该参数默认为 0，表示不开启，也就是说不对写入SQL语句条数进行控制

log_slow_admin_statements = 是否将慢管理语句记录到慢查询的日志中

[命令]

查看慢查询记录数 = SHOW GLOBAL STATUS LIKE '%Slow_queries%'

查看慢查询相关配置 = show variables like '%slow_query_log%'
```

# 第五章 附录


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

4. 常见配置项

   ```mysql
   #每次事务的 redo log 都直接持久化到磁盘
   innodb_flush_log_at_trx_commit = 1
   
   #每次事务的 binlog 都持久化到磁盘
   sync_binlog = 1
   
   #事务隔离级别
   read-uncommitted：读未提交，允许脏读
   read-committed：读提交，不允许脏读，但允许不可重复读
   repeatable-read：可重复读，不允许脏读、不可重复读，但允许幻读
   serializable：串行化，以上都不允许
   
   #建议设置为读提交
   transaction_isolation=read-committed
   ```

5. 数据库对比工具

   ```ini
   ;每次发布外网时,把外网的库备份导入到内网,然后对比生成差异sql
   tool = mysqldbcompare  
   
   cmd = mysqldbcompare --server1=user:pass@host:port:socket --server2=user:pass@host:port:socket db1:db2
   ```




# 第五章 navicat 用法

1. 创建连接时，可以设置ssh通道(服务器的3306端口不暴露于公网)

2. 工具--> 结构同步：用于对比开发环境和正式环境的数据库差异

3. 工具--->命令列：和mysql的客户端一样

4. 新建查询：打开一个查询标签页面

5. 清空表 vs 截断表

   ```ini
   [清空表]
   sql   	  	  = DELETE FROM table_name
   返回值 		= 返回删除行数
   自增字段处理    = 不会重置自增字段
   效率           = 扫描全表，表数据越多越慢
   日志           = 会记录日志，可恢复
   
   [截断表]
   sql   	  	  = TRUNCATE [TABLE] table_name
   返回值 		= 返回0
   自增字段处理    = 自增字段重置为初始值
   效率           = 不扫描全表，效率高
   日志           = 不会记录日志，无法恢复
   ```

6. 运行sql文件：常用于导入某个表或者某个数据库

7. 转储sql文件：常用于备份某个表或者某个数据库

8. 删除表：drop Table table_name

