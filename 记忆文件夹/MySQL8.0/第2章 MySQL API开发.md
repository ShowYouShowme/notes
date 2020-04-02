# 数据库完成连接登录

+ 相关函数

```c++
MYSQL *STDCALL mysql_real_connect(MYSQL *mysql, const char *host,
                                  const char *user, const char *passwd,
                                  const char *db, unsigned int port,
                                  const char *unix_socket,
                                  unsigned long clientflag);
int STDCALL mysql_options(MYSQL *mysql, enum mysql_option option,
                          const void *arg);
int STDCALL mysql_ping(MYSQL *mysql);
```
+ 代码演示

```c++
int main()
{
	MYSQL mysql;
	mysql_init(&mysql);
	const char *host = "127.0.0.1";
	const char *user = "root";
	const char *pass = "123456";
	const char *db = "laoxiaketang";

	//连接登录数据库
	if (!mysql_real_connect(&mysql,host,user,pass,db,3306,nullptr,0))
	{
		cout << "mysql connect failed." << mysql_error(&mysql) << endl;
		return -1;
	}
	else
	{
		cout << "mysql connect" << host << "success!" << endl;
	}
	cout << "Hello World!" << endl;
	return 1;
}
```





# 超时设定和断线重连

```c++
#include <iostream>
#include <mysql.h>
#include <thread>
using namespace std;
int main()
{
	MYSQL mysql;
	mysql_init(&mysql);
	const char *host = "192.168.0.230";
	const char *user = "root";
	const char *pass = "123456";
	const char *db = "laoxiaketang";
	//设定超时3秒
	int to = 3;
	int re = mysql_options(&mysql, MYSQL_OPT_CONNECT_TIMEOUT, &to);
	if (re != 0)
	{
		cout << "mysql_options failed:" << mysql_error(&mysql) << endl;
	}

    //设置自动重连
	int recon = 1;
	re = mysql_options(&mysql, MYSQL_OPT_RECONNECT, &recon);
	if (re != 0)
	{
		cout << "mysql_options failed:" << mysql_error(&mysql) << endl;
	}
	//连接登录数据库
	if (!mysql_real_connect(&mysql,host,user,pass,db,3306,nullptr,0))
	{
		cout << "mysql connect failed." << mysql_error(&mysql) << endl;
		return -1;
	}
	else
	{
		cout << "mysql connect" << host << "success!" << endl;
	}
	//测试断线重连--测试方法:连接上后先关闭数据库，然后再启动数据库
	for (int i = 0; i < 1000; ++i)
	{
		int re = mysql_ping(&mysql);
		if (re == 0)
		{
			cout << host << ":mysql ping success!" << endl;
		}
		else
		{
			cout << host << ":mysql ping failed:" << mysql_error(&mysql) << endl;
		}
		this_thread::sleep_for(1s);
	}
	cout << "Hello World!" << endl;
	return 1;
}
```

# 数据查询

+ 查询步骤

  1. 执行SQL语句API

     ```c++
     //手动指定字符串长度，可以包含任意字符
     int STDCALL mysql_real_query(MYSQL *mysql, const char *q, unsigned long length);
     //sql语句以'\0'结束，字符串中不能有'\0'
     int STDCALL mysql_query(MYSQL *mysql, const char *q);
     ```

  2. 获取结果集

     1. API
     ```c++
     //接收全部结果，要考虑缓冲
     MYSQL_RES *STDCALL mysql_store_result(MYSQL *mysql);
     //通知数据库开始读数据，但并未真正读取
     MYSQL_RES *STDCALL mysql_use_result(MYSQL *mysql);
     ```
     2. mysql_store_result缓冲设定
        1. 配置文件里设置max_allowed_packet，默认64M
        2. 代码里配置选项MYSQL_OPT_MAX_ALLOWED_PACKET
  3. 遍历和清理结果集API
     
  ```c++
  //返回每一列长度，结果是二进制数据用此接口确定数据长度
  unsigned long *STDCALL mysql_fetch_lengths(MYSQL_RES *result);
  MYSQL_ROW STDCALL mysql_fetch_row(MYSQL_RES *result);
  void STDCALL mysql_free_result(MYSQL_RES *result);
  ```
  
  4. 注意:
     1. 执行单条SQL语句不用加`;`
     2. 执行SQL语句后必须获取结果集并清理，否则下次执行SQL报错


+ 代码演示

  + 执行SQL语句

  ```c++
  int main()
  {
  	MYSQL mysql;
  	mysql_init(&mysql);
  	const char *host = "192.168.0.230";
  	const char *user = "root";
  	const char *pass = "123456";
  	const char *db = "mysql";
  	//连接登录数据库
  	if (!mysql_real_connect(&mysql,host,user,pass,db,3306,nullptr,0))
  	{
  		cout << "mysql connect failed." << mysql_error(&mysql) << endl;
  		return -1;
  	}
  	else
  	{
  		cout << "mysql connect" << host << "success!" << endl;
  	}
  	const char *sql = "select * from user";
  	//返回0表示成功
  	int re = mysql_real_query(&mysql, sql, strlen(sql));
  	if (re != 0)
  	{
  		cout << "mysql_real_query failed:" << sql << mysql_error(&mysql) << endl;
  	}
  	else
  	{
  		cout << "mysql_real_query success:" << sql << endl;
  	}
  	mysql_close(&mysql);
  	mysql_library_end();
  	getchar();
  	return 1;
  }
  ```
  
  + 获取结果集
  
    ```c++
    //获取结果集 debug查看result的值即可明白两个API的区别
    //MYSQL_RES* result = mysql_use_result(&mysql);
    MYSQL_RES* result = mysql_store_result(&mysql);
    if (result == nullptr)
    {
        cout << "mysql_use_result failed:" << mysql_error(&mysql) << endl;
    }
    ```
  
  + 遍历并显示结果集
  
  ```c++
  //遍历结果集
  MYSQL_ROW row;
  while (row = mysql_fetch_row(result))
  {
      //二进制数据用此接口获取长度
      unsigned long* lens = mysql_fetch_lengths(result);
      cout << lens[0] << "[" << row[0] << "," << row[1] << "]" << endl;
  }
  //清理结果集
  mysql_free_result(result);
  ```

# 表结构获取

+ 目的：希望通过表字段名获取值，类似php
+ API

```c++
//Flag
CLIENT_OPTIONAL_RESULTSET_METADATA
MYSQL_FIELD *STDCALL mysql_fetch_field(MYSQL_RES *result);
unsigned int STDCALL mysql_num_fields(MYSQL_RES *res);
MYSQL_FIELD *STDCALL mysql_fetch_field_direct(MYSQL_RES *res,
                                              unsigned int fieldnr);
```

+ 代码示例

```c++
//获取表结构
MYSQL_FIELD *field = nullptr;
while (field = mysql_fetch_field(result))
{
    cout << "key:" << field->name << endl;
}
//获取表字段数量
int fnum = mysql_num_fields(result);
//遍历结果集
MYSQL_ROW row;
while (row = mysql_fetch_row(result))
{
    unsigned long* lens = mysql_fetch_lengths(result);
    //cout << lens[0] << "[" << row[0] << "," << row[1] << "]" << endl;
    for (int i = 0; i < fnum;++i)
    {
        cout << mysql_fetch_field_direct(result, i)->name << ":";
        if (row[i])
        {
            cout << row[i] << endl;;
        }
        else
        {
            cout << "NULL" << endl;
        }
    }
}
//清理结果集
mysql_free_result(result);
```



#  用代码创建表

+ 使用场景
  + 程序免部署
  + 以年月日小时分表
+ 示例代码

```c++
//1 创建表 表名和字段名用"`"包含,否则无法与mysql关键字相同
string sql = "CREATE TABLE IF NOT EXISTS `t_image`  ( \
		`id` int AUTO_INCREMENT,\
		`name` varchar(1024),\
		`path` varchar(2046),\
		`size` int,\
		PRIMARY KEY(`id`)\
		) ";
int re = mysql_query(&mysql, sql.c_str());
if (re != 0)
{
    cout << "mysql_query:" << mysql_error(&mysql) << endl;
}
```



# 插入1千条数据

+ API

```c++
my_ulonglong STDCALL mysql_insert_id(MYSQL *mysql);
```

+ 代码示例

```c++
for (int i = 0;i < 1000; ++i)
{
    stringstream ss;
    ss << "insert `t_image` (`name`,`path`,`size`) values('image";
    ss << i << ".jpg'" << ",'d:/img/',10240)";
    sql = ss.str();
    re = mysql_query(&mysql, sql.c_str());
    if (re == 0)
    {
        int count = mysql_affected_rows(&mysql);
        cout << "mysql_affected_rows " << count << ",insert id:"<< mysql_insert_id(&mysql) << endl;
    }
    else
    {
        cout << "insert failed:" << mysql_error(&mysql) << endl;
    }
}
```



# update修改数据

示例代码

```c++
//sql语句直接写死
sql = "update t_image set `name`='test1.png', `size`= 4999 where `id` = 1";
re = mysql_query(&mysql, sql.c_str());
if (re == 0)
{
    int count = mysql_affected_rows(&mysql);
    cout << "mysql_affected_rows " << count << endl;
}
else
{
    cout << "update failed:" << mysql_error(&mysql) << endl;
}
```

```c++
//sql语句由map拼装出来
map<string, string> kv;
kv["name"] = "wzc";
kv["size"] = "195";
string where = " where id = 1";
stringstream ss;
ss << "update `t_image` set ";
for (auto it = kv.begin(); it != kv.end(); ++it)
{
    ss << "`" << it->first << "` ='" << it->second << "',";
}
string tmp = ss.str();
tmp.pop_back();
tmp += where;
sql = tmp;
re = mysql_query(&mysql, sql.c_str());
if (re != 0)
{
    cout << "update error:" << mysql_error(&mysql) << endl;
}
else
{
    cout << "mysql_affected_rows:" << mysql_affected_rows(&mysql) << endl;
}
```



# 清理数据

+ 清理方法

```mysql
/*不真正删除数据，仅做标识，可以事务回滚，速度慢,自增ID不会重置*/
/*OPTMIZE TABLE t_image 会清理数据*/
delete from t_image
/*清空整个表，重置自增ID*/
truncate t_image
/*删除整个表，包括表结构，几乎不用*/
drop table t_image
```

+ 示例代码

```c++
//删除整个表--不会实际删除空间，查看ibd文件验证
sql = "delete from t_image";
re = mysql_query(&mysql, sql.c_str());
if (re == 0)
{
    int count = mysql_affected_rows(&mysql);
    cout << "mysql_affected_rows " << count << endl;
}
else
{
    cout << "delete failed:" << mysql_error(&mysql) << endl;
}
```

```c++
//优化 实际清理空间
sql = "OPTIMIZE TABLE t_image";
re = mysql_query(&mysql, sql.c_str());
if (re == 0)
{
    int count = mysql_affected_rows(&mysql);
    cout << "mysql_affected_rows " << count << endl;
}
else
{
    cout << "OPTIMIZE failed:" << mysql_error(&mysql) << endl;
}
```

```c++
//删除满足指定条件的数据--不会实际删除空间
sql = "delete from t_image where id = 1";
re = mysql_query(&mysql, sql.c_str());
if (re == 0)
{
    int count = mysql_affected_rows(&mysql);
    cout << "mysql_affected_rows " << count << endl;
}
else
{
    cout << "delete failed:" << mysql_error(&mysql) << endl;
}
```

```c++
//清空数据，回复自增ID从1开始
sql = "truncate t_image";
re = mysql_query(&mysql, sql.c_str());
if (re == 0)
{
    int count = mysql_affected_rows(&mysql);
    cout << "mysql_affected_rows " << count << endl;
}
else
{
    cout << "delete failed:" << mysql_error(&mysql) << endl;
}
```



# 执行多条SQL语句

+ API

```c++
//Flag
CLIENT_MULTI_STATEMENTS
//指针移至下个结果
int STDCALL mysql_next_result(MYSQL *mysql);
//同步获取影响行数
my_ulonglong STDCALL mysql_affected_rows(MYSQL *mysql);
```

```c++
#include <iostream>
#include <mysql.h>
#include <thread>
#include <string>
#include <sstream>
#include <map>
using namespace std;
int main()
{
	MYSQL mysql;
	mysql_init(&mysql);
	const char *host = "127.0.0.1";
	const char *user = "root";
	const char *pass = "123456";
	const char *db = "laoxiaketang";
	//连接登录数据库
	if (!mysql_real_connect(&mysql, host, user, pass, db, 3306, nullptr, CLIENT_MULTI_STATEMENTS))
	{
		cout << "mysql connect failed." << mysql_error(&mysql) << endl;
		return -1;
	}
	else
	{
		cout << "mysql connect" << host << "success!" << endl;
	}

	//1 创建表
	string sql = "CREATE TABLE IF NOT EXISTS `t_image`  ( \
		`id` int AUTO_INCREMENT,\
		`name` varchar(1024),\
		`path` varchar(2046),\
		`size` int,\
		PRIMARY KEY(`id`)\
		);";

	//清空数据，回复自增ID从1开始
	sql += "truncate t_image;";

	//2 插入数据 返回影响行号
	for (int i = 0;i < 100; ++i)
	{
		stringstream ss;
		ss << "insert `t_image` (`name`,`path`,`size`) values('image";
		ss << i << ".jpg'" << ",'d:/img/',10240);";
		sql += ss.str();
	}
	//3 修改数据
	//update t_image set name="test1.png", size= 1999 where id = 1;
	sql += "update t_image set `name`='test1.png', `size`= 4999 where `id` = 1;";


	//指定删除条件--delete不会重置ID，因此要用truncate table
	sql += "delete from t_image where id = 1;";

	//优化 实际清理空间
	sql += "select * from t_image";
	//执行sql立刻返回，但语句并未全部执行完毕,需要获取结果
	//把sql语句发送给mysql server
	int re = mysql_query(&mysql, sql.c_str());
	if (re != 0)
	{
		cout << "mysql_query failed:" << mysql_error(&mysql) << endl;
	}

	//有多个返回结果
	do 
	{
		MYSQL_RES *result = mysql_store_result(&mysql);
		if (result)
		{
			cout << "mysql_num_rows = " << mysql_num_rows(result) << endl;
			mysql_free_result(result);
		}
		else //INSERT UPDATE DELETE CREATE DROP TRUNCATE 或者SELECT ERROR
		{
			//有字段无结果集 select出错
			if (mysql_field_count(&mysql) > 0)
			{
				cout << "No retrieve result!" << endl;
			}
			else
			{
				//同步等待服务器处理结果,这一步是必需的
				cout << mysql_affected_rows(&mysql) << " rows affected!"<<endl;
			}
		}
	} while (mysql_next_result(&mysql) == 0);//取下条结果
	mysql_close(&mysql);
	mysql_library_end();
	cout << "Hello World!" << endl;
	getchar();
	return 1;
}
```

