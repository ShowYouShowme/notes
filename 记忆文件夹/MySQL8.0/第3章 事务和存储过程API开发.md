# 事务特性和用法介绍

+ 定义：多条 SQL 语句要么全部执行，要么全部不执行

+ 使用事务

  ```mysql
  START TRANSACTION
  set autocommit = 0
  SQL语句
  ROLLBACK[optional]
  COMMIT
  set autocommit = 1
  ```
  
+ 引擎对比

  + MyISAM
    + 不支持事务回滚
    + 不支持行锁，仅支持表锁
    + 查询速度快
  + **InnoDB**
    + 支持事务回滚
    + 支持表锁和行锁
  
+ 代码演示

```c++
#include <iostream>
#include <mysql.h>
#include <thread>
#include <string>
#include <sstream>
#include <map>
#define ExecuteSQL(sql)		{\
								int re = mysql_query(&mysql, sql);\
								if (re != 0)\
								{\
									cout << "mysql_query failed:" << mysql_error(&mysql) << endl;\
								}\
							}
using namespace std;
int main()
{
	MYSQL mysql;
	mysql_init(&mysql);
	const char *host = "192.168.0.230";
	const char *user = "root";
	const char *pass = "123456";
	const char *db = "laoxiaketang";
	//连接登录数据库
	if (!mysql_real_connect(&mysql, host, user, pass, db, 3306, nullptr, 0))
	{
		cout << "mysql connect failed." << mysql_error(&mysql) << endl;
		return -1;
	}
	else
	{
		cout << "mysql connect" << host << "success!" << endl;
	}

	//1 创建表--设置引擎为InnoDB
	string sql = "CREATE TABLE IF NOT EXISTS `t_video`  ( \
		`id` int AUTO_INCREMENT,\
		`name` varchar(1024),\
		`path` varchar(2046),\
		`size` int,\
		PRIMARY KEY(`id`)\
		) ENGINE=InnoDB;";

	ExecuteSQL(sql.c_str());

	ExecuteSQL("truncate `t_video`");
	//事务
	//1  START TRANSACTION  开始事务
	ExecuteSQL("START TRANSACTION");
	//2	set autocommit = 0 手动提交
	ExecuteSQL("set autocommit = 0");
	//3	SQL语句
	for (int i = 0; i < 3; ++i)
	{
		ExecuteSQL("insert into `t_video` (`name`) values ('test_video')");
	}
	//4	ROLLBACK[可选]
	ExecuteSQL("ROLLBACK");
	for (int i = 0; i < 10000; ++i)
	{
		ExecuteSQL("insert into `t_video` (`name`) values ('test_video')");
	}
	//5	COMMIT
	ExecuteSQL("COMMIT");
	//6	set autocommit = 1 恢复自动提交
	ExecuteSQL("set autocommit = 1");


	//select
	ExecuteSQL("select count(*) from `t_video`");
	MYSQL_RES *result = mysql_store_result(&mysql);
	if (result)
	{
		MYSQL_ROW row = mysql_fetch_row(result);
		cout << "t_video count(*):" << row[0] << endl;
	}
	mysql_close(&mysql);
	mysql_library_end();
	cout << "Hello World!" << endl;
	getchar();
	return 1;
}
```

# 性能测试

+ 单条语句插入1千条数据

```c++
auto start = system_clock::now();
for (int i = 0; i < 1000; ++i)
{
    ExecuteSQL("insert into `t_video` (`name`) values ('single')");
}
auto end = system_clock::now();
auto dur = duration_cast<milliseconds>(end - start);
cout << "单条语句插入1千条数据" << dur.count() / 1000. << endl;
```

+ 多条语句插入1千条数据

```c++
/*
	数据库连接时加上参数CLIENT_MULTI_STATEMENTS
*/
auto start = system_clock::now();
string sql;
for (int i = 0; i < 1000; ++i)
{
    sql += "insert into `t_video` (`name`) values ('single');";
}
ExecuteSQL(sql.c_str());
//要获取结果集，否则时间测试不准
do 
{
    MYSQL_RES *result = mysql_store_result(&mysql);
    if (!result)
    {
        //这一步是必需的
        cout << mysql_affected_rows(&mysql) << endl;
    }
} while (mysql_next_result(&mysql) == 0);
auto end = system_clock::now();
auto dur = duration_cast<milliseconds>(end - start);
cout << "多条语句插入1千条数据" << dur.count() / 1000. << endl;
```

+ 事务插入1千条数据

```c++
auto start = system_clock::now();
//1  START TRANSACTION  开始事务
ExecuteSQL("START TRANSACTION");
//2	set autocommit = 0 手动提交
ExecuteSQL("set autocommit = 0");
//3	SQL语句
for (int i = 0; i < 1000; ++i)
{
    ExecuteSQL("insert into `t_video` (`name`) values ('test_video')");
    cout << mysql_affected_rows(&mysql) << endl;
}
//5	COMMIT
ExecuteSQL("COMMIT");
//6	set autocommit = 1 恢复自动提交
ExecuteSQL("set autocommit = 1");
auto end = system_clock::now();
auto dur = duration_cast<milliseconds>(end - start);
cout << "事务插入1千条数据" << dur.count() / 1000. << endl;
```

# 插入、读取图片

+ API

```c++
MYSQL_STMT *STDCALL mysql_stmt_init(MYSQL *mysql);
int STDCALL mysql_stmt_prepare(MYSQL_STMT *stmt, const char *query,
                               unsigned long length);
bool STDCALL mysql_stmt_bind_param(MYSQL_STMT *stmt, MYSQL_BIND *bnd);
int STDCALL mysql_stmt_execute(MYSQL_STMT *stmt);
my_ulonglong STDCALL mysql_stmt_affected_rows(MYSQL_STMT *stmt);
bool STDCALL mysql_stmt_close(MYSQL_STMT *stmt);
const char *STDCALL mysql_stmt_error(MYSQL_STMT *stmt);
```

+ 写入图片

```c++
#include <iostream>
#include <mysql.h>
#include <string>
#include <fstream>
#include <vector>
using namespace std;

int main()
{
	MYSQL mysql;
	mysql_init(&mysql);
	const char *host = "192.168.0.230";
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

	//1 创建存放二进制数据的表 t_data
	string sql = "CREATE TABLE IF NOT EXISTS `t_data`  ( \
		`id` INT NOT NULL AUTO_INCREMENT,\
		`name` VARCHAR(1024) NULL,\
		`data` BLOB NULL,\
		`size` INT NULL,\
		PRIMARY KEY(`id`))\
		ENGINE = InnoDB\
		DEFAULT CHARACTER SET = utf8\
		COLLATE = utf8_bin";

	//1 创建表
	int re = mysql_query(&mysql, sql.c_str());
	if (re != 0)
	{
		cout << "mysql_query:" << mysql_error(&mysql) << endl;
	}
	//2 清空表
	sql = "TRUNCATE `t_data`";
	re = mysql_query(&mysql, sql.c_str());
	if (re != 0)
	{
		cout << "mysql_query:" << mysql_error(&mysql) << endl;
	}
	//3 初始化stmt
	MYSQL_STMT *stmt = mysql_stmt_init(&mysql);
	if (stmt == nullptr)
	{
		cout << "mysql_stmt_init:" << mysql_stmt_error(stmt) << endl;
	}

	//打开并读取文件
	string filename = "mysql.jpg";
	fstream in(filename, ios::in | ios::binary);
	if (in.is_open() == false)
	{
		cout << "open file " << filename << " failed!" << endl;
		return -1;
	}
	in.seekg(0, ios::end);
	int filesize = in.tellg();
	in.seekg(0, ios::beg);
	//--不要new 数据
	vector<char> data(filesize,'\0');
	int readed = 0;//已经读了多少,不能保证一次读完!
	while (!in.eof())
	{
		in.read(&data[0] + readed, filesize - readed);
		if (in.gcount() <= 0)
			break;
		readed += in.gcount();
	}
	in.close();
	//4 预处理sql语句
	sql = "INSERT INTO `t_data` (name,data,size) VALUES(?,?,?)";
	if (mysql_stmt_prepare(stmt, sql.c_str(),sql.size()) != 0)
	{
		cout << "mysql_stmt_prepare:" << mysql_stmt_error(stmt) << endl;
	}

	//5 绑定字段
	MYSQL_BIND bind[3] = { 0 };
	bind[0].buffer_type = MYSQL_TYPE_STRING;
	bind[0].buffer = (char*)filename.c_str();
	bind[0].buffer_length = filename.size();

	bind[1].buffer_type = MYSQL_TYPE_BLOB;
	bind[1].buffer = &data[0];
	bind[1].buffer_length = filesize;

	bind[2].buffer_type = MYSQL_TYPE_LONG;
	bind[2].buffer = &filesize;

	if (mysql_stmt_bind_param(stmt, bind) != 0)
	{
		cerr << "mysql_stmt_bind_param failed:" << mysql_stmt_error(stmt) << endl;
	}

	//执行stmt sql
	if (mysql_stmt_execute(stmt) != 0)
	{
		cerr << "mysql_stmt_execute failed:" << mysql_stmt_error(stmt) << endl;
	}
	data.resize(0);//清理数据

	mysql_stmt_close(stmt);
	mysql_close(&mysql);
	mysql_library_end();
	cout << "Hello World!" << endl;
	getchar();
	return 1;
}
```
+ 读取图片

```c++
sql = "select * from `t_data`";
re = mysql_query(&mysql, sql.c_str());
if (re != 0)
{
    cout << "mysql_query:" << mysql_error(&mysql) << endl;
}
MYSQL_RES *result = mysql_store_result(&mysql);
if (!result)
{
    cerr << "mysql_store_result failed:" << mysql_error(&mysql) << endl;
}
//取一行数据
MYSQL_ROW row = mysql_fetch_row(result);
if (row == nullptr)
{
    cerr << "mysql_fetch_row failed:" << mysql_error(&mysql) << endl;
}
cout << row[0] << ":" << row[1] << ":" << row[3] << endl;
//获取每列数据大小
unsigned long *lens = mysql_fetch_lengths(result);
int fnum = mysql_num_fields(result);
for (int i = 0;i < fnum; ++i)
{
    cout << "[" << lens[i] << "]" << endl;
}
filename = "out_";
filename += row[1];
fstream out(filename, ios::out | ios::binary);
if (!out.is_open())
{
    cerr << "open file " << filename << " failed!" << endl;
}
out.write(row[2], lens[2]);//写入缓冲,不需要像read一样多次执行
out.close();
```



# 存储过程

+ 创建存储过程

  ```mysql
  /*常见存储过程*/
  CREATE PROCEDURE `p_1`(IN p_in INT, OUT p_out INT, INOUT p_inout INT)
  BEGIN
  SELECT p_in,p_out,p_inout;/*返回到结果集*/
  SET p_in = 100, p_out = 200, p_inout = 300;
  SELECT p_in, p_out, p_inout;
  END
  ```

  

+ 调用存储过程

  + 参数传递

    + stmt
    + 用代码

    ```mysql
    /*调用存储过程*/
    SET @A = 1;
    SET @B = 2;
    SET @C = 3;
    call p1(@A,@B,@C);
    select @A,@B,@C;
    ```

+ 代码演示

```c++
#include <iostream>
#include <mysql.h>
#include <string>
#include <fstream>
#include <vector>
using namespace std;

int main()
{
	MYSQL mysql;
	mysql_init(&mysql);
	const char *host = "192.168.0.230";
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



	//1 创建存储过程
	string sql;
	sql = "CREATE PROCEDURE `p_test`(IN p_in INT, OUT p_out INT, INOUT p_inout INT) \
			BEGIN \
			SELECT p_in,p_out,p_inout;\
			SET p_in = 100,p_out = 200,p_inout = 300;\
			SELECT p_in,p_out,p_inout;\
			END";
	int re = mysql_query(&mysql, sql.c_str());
	if (re != 0)
	{
		cout << "mysql_query:" << mysql_error(&mysql) << endl;
	}
	
	// 定义变量并赋值
	cout << "IN A=1,B=2,C=3" << endl;
	sql = "SET @A=1;SET @B=2;SET @C=3;";
	re = mysql_query(&mysql, sql.c_str());
	if (re != 0)
	{
		cout << "mysql_query:" << mysql_error(&mysql) << endl;
	}
	do 
	{
		cout << "SET affect:" << mysql_affected_rows(&mysql) << endl;
	} while (mysql_next_result(&mysql) == 0);

	//调用存储过程
	sql = "call `p_test`(@A,@B,@C)";
	re = mysql_query(&mysql, sql.c_str());
	if (re != 0)
	{
		cout << "mysql_query:" << mysql_error(&mysql) << endl;
	}
	cout << "IN Proc:";
	do 
	{
		MYSQL_RES *res = mysql_store_result(&mysql);
		if (res == nullptr)
			continue;
		//打印结果集
		int fcount = mysql_num_fields(res);
		for (;;)
		{
			//提取一行记录
			MYSQL_ROW row = mysql_fetch_row(res);
			if (row == nullptr) break;
			for (int i = 0; i < fcount;++i)
			{
				if (row[i])
				{
					cout << row[i] << " ";
				}
				else
				{
					cout << "NULL" << " ";
				}
			}
			cout << endl;
		}
		mysql_free_result(res);
	} while (mysql_next_result(&mysql) == 0);
	//获取存储过程结果
	sql = "select @A,@B,@C";
	re = mysql_query(&mysql, sql.c_str());
	if (re != 0)
	{
		cout << "mysql_query:" << mysql_error(&mysql) << endl;
	}
	MYSQL_RES *res = mysql_store_result(&mysql);
	MYSQL_ROW row = mysql_fetch_row(res);
	cout << "in=" << row[0] << " out:" << row[1] << " inout:" << row[2] << endl;
	mysql_free_result(res);

	mysql_close(&mysql);
	mysql_library_end();
	cout << "Hello World!" << endl;
	getchar();
	return 1;
}
```

