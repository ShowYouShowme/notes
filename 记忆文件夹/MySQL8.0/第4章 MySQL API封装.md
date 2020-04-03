#  封装策略

+ 隐藏mysql
  + 可任意替换为其它数据库api
  + 调用者不需要引用MySQL头文件
+ 可扩展线程安全
  + 公共变量尽量不放到成员里，每个公共变量都涉及线程安全
  + 此版本暂时不做

+ 简化数据接口
  + 利用map和vector等容器
+ 可扩展附加功能
  + 字符集转换
  + 文件存取
+ 跨平台
  + windows：VS2017
  + linux：g++ 和makefile



# LXMysql动态链接库和测试vs2017项目创建

dll项目配置

1. Debug x64
2. 删掉除了`LXMysql.h`和`LXMysql.cpp`外的文件
3. 不使用**预编译头**
4. 设置输出目录：`常规--输出目录`
5. 设置输出lib文件：`链接器--高级--导入库`
6. 配置MySQL依赖：
   - 头文件包含目录：`C/C++--常规--附加包含目录`
   - lib文件目录：`链接器--常规--附加库目录`
   - 依赖的lib文件名：`链接器--输入--附加依赖项`

解决方案配置

1. 设置启动项目：`test_LXMysql`
2. 项目依赖项：`项目test_LXMysql依赖于LXMysql`

test_LXMysql项目配置
1. Debug x64
2. 设置输出目录：`常规--输出目录`
3. 设置工作目录：`调试--工作目录`
4. 配置DLL项目依赖：
   - 设置头文件包含目录：`C/C++--常规--附加包含目录`
   - 设置第三方库目录：`链接器--常规--附加库目录`
   - 设置用到的库：`链接器--输入--附加依赖项`



# 完成封装Init和Close接口

思路：一个连接对应一个LXMysql对象

问题：资源何时清理？

1. 在析构函数里清理，此时要确保客户**只能用指针操作LXMysql对象**或者**禁止LXMysql的copy构造和copy赋值函数**
2. 由用户自己清理

代码演示

```c++
/*LXMysql.h*/
struct MYSQL;
class  LXAPI LXMysql
{
public:
	//初始化MySQL API
	bool Init();

	//清理占用资源
	void Close();
protected:
	MYSQL *mysql = nullptr;
};
```

```c++
/*LXMysql.cpp*/
bool LXMysql::Init()
{
	cout << "LXMysql::Init()" << endl;
	//新建一个MYSQL对象
	this->mysql = mysql_init(nullptr);
	if (!this->mysql)
	{
		cerr << "mysql_init failed:" << endl;
	}
	return true;
}
void LXMysql::Close()
{
	if (this->mysql)
	{
		mysql_close(this->mysql);
		this->mysql = nullptr;
	}
	cout << "LXMysql::Close()" << endl;
}
```



# 完成Connect连接数据的接口

```c++
bool LXMysql::Connect(const char* host, const char* user, const char* pass,  const char* db, unsigned short port /*= 3306*/, unsigned long flag /*= 0*/)
{
    if (this->mysql == nullptr && this->Init() == false)
    {
        cerr << "MySQL Connect failed: mysql is not init!" << endl;
        return false;
    }
	if (!mysql_real_connect(this->mysql, host, user, pass, db, port, nullptr, flag))
	{
		cerr << "mysql_real_connect failed:" << mysql_error(this->mysql) << endl;
		return false;
	}
	cout << "mysql_real_connect success" << endl;
	return true;
}
```



# 完成Query执行sql语句的接口封装

```c++
bool LXMysql::Query(const char* sql, unsigned long sqllen /*= 0*/)
{
	if (this->mysql == nullptr)
	{
		cerr << "LXMysql::Query failed:mysql is NULL" << endl;
		return false;
	}
	if (sql == nullptr)
	{
		cerr << "sql is NULL" << endl;
		return false;
	}
	if (sqllen <= 0)
	{
		sqllen = strlen(sql);
	}
	if (sqllen <= 0)
	{
		cerr << "Query sql is empty!" << endl;
		return false;
	}
	int re = mysql_real_query(this->mysql, sql, sqllen);
	if (re != 0)
	{
		cerr << "mysql_real_query failed:" << mysql_error(this->mysql) << endl;
		return false;
	}
	return true;
}
```





# 完成Options接口封装

```c++
bool LXMysql::Options(LX_OPT opt, const void* arg)
{
	if (this->mysql == nullptr)
	{
		cerr << "LXMysql::Query failed:mysql is NULL" << endl;
		return false;
	}
	int re = mysql_options(this->mysql, (mysql_option)opt, arg);
	if (re != 0)
	{
		cerr << "mysql_options failed:" << mysql_error(this->mysql) << endl;
		return false;
	}
	return true;
}

bool LXMysql::SetConnectTimeout(int sec)
{
	return this->Options(LX_OPT_CONNECT_TIMEOUT, &sec);
}

bool LXMysql::SetReconnect(bool isre /*= true*/)
{
	return this->Options(LX_OPT_RECONNECT, &isre);
}

```



# 完成结果集获取StoreResult和清理接口

```c++
bool LXMysql::StoreResult()
{
    if (this->mysql == nullptr)
    {
        cerr << "LXMysql::StoreResult failed:mysql is NULL" << endl;
        return false;
    }
    this->FreeResult();
    this->result = mysql_store_result(this->mysql);
    //mysql_store_result 返回NULL不一定是失败
    if (this->result == nullptr && mysql_errno(this->mysql) != 0)
    {
        cerr << "mysql_store_result error:" << mysql_error(this->mysql) << endl;
        return false;
    }
    return true;
}

bool LXMysql::UseResult()
{
    if (this->mysql == nullptr)
    {
        cerr << "LXMysql::UseResult failed:mysql is NULL" << endl;
        return false;
    }
    this->FreeResult();
    this->result = mysql_use_result(this->mysql);
    if (this->result == nullptr)
    {
        cerr << "mysql_use_result failed:" << mysql_error(this->mysql) << endl;
        return false;
    }
    return true;
}

void LXMysql::FreeResult()
{
    if (this->result)
    {
        mysql_free_result(this->result);
        this->result = nullptr;
    }
}
```



# 完成FetchRow获取一行vector数据

```c++
struct LXData
{
    const char* data = nullptr;
    int size = 0;
};

//为什么不用map，效仿php的方式不是更简单吗
std::vector<LXData> LXMysql::FetchRow()
{
    std::vector<LXData> re;
    if (this->result == nullptr)
    {
        return re;
    }
    MYSQL_ROW row = mysql_fetch_row(this->result);
    if (row == nullptr)
    {
        return re;
    }

    //列数
    int num = mysql_num_fields(this->result);
    for (int i = 0;i < num; ++i)
    {
        LXData data;
        data.data = row[i];
        re.push_back(data);
    }
    return re;
}
```





# 插入和修改数据封装

## 普通字符串数据

```c++
/*数据结构定义*/
struct LXAPI LXData
{
    explicit LXData(const char* data = nullptr);
    const char* data = nullptr;
    int size = 0;
};

//插入和更新用到的数据结构
using XDATA = std::map<std::string, LXData>;
```

```c++
/*将map拼成sql语句*/
std::string LXMysql::GetInsertSql(XDATA kv, std::string table)
{
    if (kv.empty() || table.empty())
    {
        return "";
    }
    stringstream ss;
    ss << "insert into `" << table << "` ";

    stringstream keys;
    keys << "(";
    stringstream vals;
    vals << " values (";
    //insert into `t_video` (`name`,`size`) values ('name1','1024');
    for (auto ptr = kv.begin();ptr != kv.end();++ptr)
    {
        keys << "`" << ptr->first << "`,";
        vals << "'" << ptr->second.data << "',";
    }

    string skeys = keys.str();
    skeys.pop_back();
    skeys += ")";
    string svals = vals.str();
    svals.pop_back();
    svals += ")";
    string sql = ss.str() + skeys + svals;
    return sql;
}

/*插入*/
bool LXMysql::Insert(XDATA kv, std::string table)
{
    if (this->mysql == nullptr)
    {
        cerr << "LXMysql::Insert failed:mysql is NULL" << endl;
        return false;
    }
    string sql = this->GetInsertSql(kv, table);
    if (sql.empty())
        return false;
    if (!this->Query(sql.c_str()))
        return false;

    int num = mysql_affected_rows(this->mysql);
    if (num <= 0)
        return false;
    return true;
}
```



## 二进制数据

