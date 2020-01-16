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

   



# 删除没有密码的用户

```shell
use mysql;
# 查看用户的权限
select host,user,password from user;

drop user 'zhangsan'@'%';

drop user '${user}'@'${host}';

# 没有名称的用户
drop user ' '@'%';

# 刷新权限
flush  privileges;
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
```

