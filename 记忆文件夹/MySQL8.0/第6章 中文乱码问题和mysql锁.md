# 字符编码类型mysql设置和转换API分析

## 涉及到编码的地方

+ Windows控制台是GBK
+ Linux控制台是UTF-8
+ 数据库用GBK保存，界面用UTF-8显示，此时要转换编码让界面显示
+ 调用API，比如windows的API用Unicode编码

## 字符编码类型

类型：
+ GBK：英文单字节，中文双字节。GB2312与GBK类似，少一部分生僻字
+ UTF-8：变长编码格式，缺点：不知道字符串占用多少字节
+ Unicode：双字节表示一个字符，wchar_t
  1. windows：UCS-2 utf-16
  2. linux：UCS-4 utf-32

<span style="color:violet;font-weight:bold">"yourString"编码类型与代码文件编码类型一致：</span>

+ vs2015及之前：GBK
+ qtcreator：utf-8
+ vs2017：utf-8
+ linux：utf-8
+ 建议：字符串从配置文件读取，这样编码类型仅与配置文件相关或者用`u8"字符串"`表示utf-8的字符串

## MySQL编码

编码设定

1. 库默认编码
2. 表默认编码
3. 字段编码设置
4. set names utf8 设定API的字符集

## C/C++转码SDK

1. STL
   - codecvt
     - codecvt_utf8
     - use_facet
     - std::locale 与本地字符集有关，如果Ubuntu没装中文，转码失败
   - 编码兼容文件
     - gcc高版本
     - vs2015-vs2017与vs2013和gcc不兼容
     - gbk转码依赖环境
   - 建议：不搞跨平台用，比如仅在linux下
2. Windows
   1. MultiByteToWideChar
   
      ```c++
      int len = MultiByteToWideChar(CP_UTF8,//源字符串编码类型
      0,//默认转换方式
      data,//源字符串
      -1,//字符串大小,-1表示找'\0'结束
      nullptr,//输出
      0//输出空间大小
      );
      
      MultiByteToWideChar(CP_UTF8, 0, data, -1, (wchar_t*)udata.data(), len);
      ```
   
   2. WideCharToMultiByte
3. linux
   1. iconv_open
   2. iconv
   3. iconv_close

# windows上字符集gbk和utf8互转

## utf-8转GBK



1. utf-8字符串怎么来
   - u8"我是UTF-8字符串"
   - 从UTF-8编码的文件读取
2. 如何测试转换结果？<br/>控制台打印

```c++
//转换为Unicode
wstring ToUnicode(UINT CodePage, const char* data)
{
	wstring ws;
	//1 UTF8 转换为 UNICODE
	int len = MultiByteToWideChar(CodePage,
		0,
		data,
		strlen(data),
		nullptr,
		0);
	if (len <= 0)
		return ws;
	ws.resize(len);
	MultiByteToWideChar(CodePage,
		0,
		data,
		strlen(data),
		(wchar_t*)ws.data(),
		len);
	return ws;
}

//Unicode转换为其它编码
string FromUnicode(UINT CodePage, const wstring& ws)
{
	string re;
	int len = WideCharToMultiByte(CodePage,
		0,
		ws.data(),
		ws.size(),
		nullptr,
		0,
		nullptr,
		nullptr);
	if (len <= 0)
		return re;
	re.resize(len);
	WideCharToMultiByte(CodePage,
		0,
		ws.data(),
		ws.size(),
		(char*)re.data(),
		re.size(),
		nullptr,
		nullptr);
	return re;
}
```



```c++
string UTF8ToGBK(const char* data)
{
	
	//1 UTF-8 转换为UNICODE
	wstring ws = ToUnicode(CP_UTF8, data);
	//2 UNICODE 转换为UTF-8
	return FromUnicode(CP_ACP, ws);
}

int main()
{
    std::cout << "Hello World!\n"; 
	//1 测试UTF-8转GBK
	cout << UTF8ToGBK(u8"测试UTF-8转GBK") << endl;
    
    //以下的方式为实际项目用到的
    fstream fs("utf8.txt", ios::in);//utf8.txt文件以utf8编码保存
	if (!fs.is_open())
		return -1;
	string utf8;
	fs >> utf8;
	fs.close();
	cout << "utf8 转换前:" << utf8 << endl;
	cout << "utf8 转换后:" << UTF8ToGBK(utf8.c_str()) << endl;
	getchar();
	return 1;
}
```



## GBK转utf-8

1. GBK字符串怎么来
   1. 字符串前不加`u8`且代码文件用GBK编码保存
   2. 从gbk编码的文件中读取
2. 如何测试
   1. 将转换后的结果写入文件里
   2. 将转换后的结果再转换为GBK然后控制台打印

```c++
string GBKToUTF8(const char* data)
{

	//1 UTF-8 转换为UNICODE
	wstring ws = ToUnicode(CP_ACP, data);
	//2 UNICODE 转换为UTF-8
	return FromUnicode(CP_UTF8, ws);

}

int main()
{
    std::cout << "Hello World!\n"; 


	// 测试GBK到UTF-8的转换(先确保代码是GBK保存的)
	string utf8 = GBKToUTF8("测试GBK转UTF8再转为GBK");
	cout << "utf8=" << utf8 << endl;
	cout << UTF8ToGBK(utf8.c_str()) << endl;
    
    //以下方式是实际项目用的,推荐
    fstream fs;
	fs.open("gbk.txt", ios::in);//gbk.txt文件用gbk编码保存
	if (!fs.is_open())
		return -1;
	string gbk;
	fs >> gbk;
	cout << "gbk 转换前:" << gbk << endl;
	string utf8 = GBKToUTF8(gbk.c_str());
	cout << "gbk 转换后:" << utf8 << endl;
	cout << "gbk 2次转换:" << UTF8ToGBK(utf8.c_str()) << endl;
	fs.close();
    
	getchar();
	return 1;
}
```



# linux上字符集GBK和UTF8互转

1. 源文件必须用utf-8编码保存

2. 演示代码

```c++
// 代码只能在Linux上面运行
#include <iostream>
#include <iconv.h>
#include <string>
#include <fstream>
#include <string.h>
using namespace std;

static size_t Convert(char *from_cha, char *to_cha, char *in, size_t inlen, char *out, size_t outlen)
{
	//转换上下文
	iconv_t cd;
	cd = iconv_open(to_cha,from_cha);
	if (cd == nullptr)
		return -1;
	memset(out, 0, outlen);
	//返回转换字节数的数量，但是转GBK经常不正确 >=0表示成功
	size_t re = iconv(cd, &in, &inlen, &out, &outlen);
	if(cd != nullptr)
		iconv_close(cd);
    return re;
}

static string Convert(char *from_cha, char *to_cha, const char* data)
{
	string re;
	re.resize(10240);//这里可能是坑
	int inlen = strlen(data);
	Convert(from_cha, to_cha, (char*)data, inlen, (char*)re.data(), re.size());
	int outlen = strlen(re.data());
	re.resize(outlen);
	return re;
}

string UTF8ToGBK(const char* data)
{
	return Convert((char*)"utf-8", (char*)"gbk", data);
}
string GBKToUTF8(const char* data)
{
	return Convert((char*)"gbk", (char*)"utf-8",  data);
}
int main()
{
	{
		fstream fs("utf8.txt", ios::in);
		if (!fs.is_open())
			return -1;
		string utf8;
		fs >> utf8;
		fs.close();
		cout << "utf8 转换前:" << utf8 << endl;
		cout << "utf8 转换后:" << UTF8ToGBK(utf8.c_str()) << endl;
		cout << "2次转换:" << GBKToUTF8(UTF8ToGBK(utf8.c_str()).c_str()) << endl;
	}

	{
		cout << "++++++++++++++++++++++++++++++++++" << endl;
		fstream fs;
		fs.open("gbk.txt", ios::in);
		if (!fs.is_open())
			return -1;
		string gbk;
		fs >> gbk;
		cout << "gbk 转换前:" << gbk << endl;
		string utf8 = GBKToUTF8(gbk.c_str());
		cout << "gbk 转换后:" << utf8 << endl;
		fs.close();
	}

	getchar();
	return 1;
}
```



# LXMysql库添加字符集转换函数并测试GBK和UTF8数据插入和读取

1. 接口

   ```c++
   std::string LXData::UTF8ToGBK()
   {
       return __UTF8ToGBK((char*)this->data);
   }
   std::string LXData::GBKToUTF8()
   {
       return __GBKToUTF8((char*)this->data);
   }
   ```

2. 插入和读取GBK数据

   ```c++
   //插入GBK的数据
   sql = "CREATE TABLE IF NOT EXISTS `t_gbk` \
   			(`id` INT AUTO_INCREMENT,\
   			 `name` VARCHAR(1024) CHARACTER SET gbk COLLATE gbk_bin,\
   			PRIMARY KEY(`id`))";
   my.Query(sql.c_str());
   
   //清空数据
   my.Query("truncate t_gbk");
   //指定SQL语句使用的编码
   my.Query("set names gbk");
   
   {
       XDATA data;
       LXData tmp(u8"测试的GBK中文!");
       string gbk = tmp.UTF8ToGBK();
       data["name"] = LXData(gbk.c_str());
       my.Insert(data, "t_gbk");
   }
   cout << "=============Print gbk string===========" << endl;
   my.Query("set names gbk");
   my.Query("select * from `t_gbk`");
   my.StoreResult();
   for (;;)
   {
       auto row = my.FetchRow();
       if (row.size() == 0)
       {
           break;
       }
       #if _WIN32
       cout << "id:" << row[0].data << " name:" << row[1].data << endl;
       #else
       cout << "id:" << row[0].data << " name:" << row[1].GBKToUTF8() << endl;
       #endif
   }
   my.FreeResult();
   ```

3. 插入和读取UTF-8数据

   ```c++
   sql = "CREATE TABLE IF NOT EXISTS `t_utf8` \
   			(`id` INT AUTO_INCREMENT,\
   			 `name` VARCHAR(1024) CHARACTER SET utf8 COLLATE utf8_bin,\
   			PRIMARY KEY(`id`))";
   my.Query(sql.c_str());
   //清空数据
   my.Query("truncate t_utf8");
   //指定SQL语句使用的编码
   my.Query("set names utf8");
   
   XDATA data;
   data["name"] = LXData(u8"测试的UTF中文!");
   my.Insert(data, "t_utf8");
   cout << "=============Print utf8 string===========" << endl;
   my.Query("set names utf8");
   my.Query("select * from `t_utf8`");
   my.StoreResult();
   for (;;)
   {
       auto row = my.FetchRow();
       if (row.size() == 0)
       {
           break;
       }
       #if _WIN32
       cout << "id:" << row[0].data << " name:" << row[1].UTF8ToGBK() << endl;
       #else
       cout << "id:" << row[0].data << " name:" << row[1] << endl;
       #endif
   }
   my.FreeResult();
   ```

   

# 简易获取数据的接口GetResult实现

```c++
typedef std::vector<std::vector<LXData>> XROWS;	
LX::XROWS LXMysql::GetResult(const char* sql)
{
    this->FreeResult();
    XROWS rows;
    if (!this->Query(sql))
        return rows;
    if (!this->StoreResult())
        return rows;
    for (;;)
    {
        auto row = this->FetchRow();
        if (row.empty())
            break;
        rows.push_back(row);
    }
    return rows;
}
```



# mysql的表锁和行锁代码示例购票竞争

## 表锁

1. lock table t_image read;共享锁
2. lock table t_image write;排它锁
3. unlock tables

## 行锁

```c++
sql = "CREATE TABLE IF NOT EXISTS `t_tickets` \
			(`id` INT AUTO_INCREMENT,\
			 `sold` INT,\
			PRIMARY KEY(`id`))";
my.Query(sql.c_str());

{
    XDATA data;
    data["sold"] = LXData("0");
    my.Insert(data, "t_tickets");
    my.Insert(data, "t_tickets");
    my.Insert(data, "t_tickets");
    my.Insert(data, "t_tickets");
    my.StartTransaction();
    XROWS rows = my.GetResult("select * from `t_tickets` where sold = 0 order by id for update");

    cout << "buy ticket id is:" << rows[0][0].data << endl;

    //模拟冲突
    this_thread::sleep_for(10s);
    string where = "where id=";
    where += rows[0][0].data;
    data["sold"] = LXData("1");
    cout << "更新结果:" << my.Update(data, "t_tickets", where) << endl;
    //my.GetResult("select * from `t_tickets` where sold = 0 for update");
    my.Commit();
    my.StopTransaction();
}
```

