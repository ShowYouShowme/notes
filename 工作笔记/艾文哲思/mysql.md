# 导出数据

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
   service mysql stop
   ```

4. 启动服务

   ```shell
   service mysql start
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

