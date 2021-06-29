# 第一章 安装

C++ 开发一定要用Boost，里面集成了异步IO，Http和websocket 协议处理，json解析，各种字符串操作等等，非常省事。另外Boost还可以非常方便地操作Python



## 1.1 下载源码

```shell
wget https://boostorg.jfrog.io/artifactory/main/release/1.70.0/source/boost_1_70_0.zip
```



## 1.2 解压和安装

```shell
unzip boost_1_70_0.zip

cd ./boost_1_70_0

./bootstrap.sh --prefix=/usr  --with-libraries=all # 编译全部库

./b2 install
```



## 1.3 示例代码

+ 代码

  ```C++
  #include <boost/version.hpp>
  #include <boost/config.hpp>
  #include <boost/lexical_cast.hpp>
  #include <iostream>
  using namespace std;
  int main()
  {
      using boost::lexical_cast;
      int a= lexical_cast<int>("123456");
      double b = lexical_cast<double>("123.456");
      std::cout << a << std::endl;
      std::cout << b << std::endl;
      return 0;
  }
  ```

+ 编译

  ```shell
  g++ ./boost_test.cpp
  
  ./a.out # 可以查看到输出数据
  ```




# 第二章 数据处理



## 2.1 json

1. 链接的库：boost_json

2. 头文件：#include <boost/json.hpp>

3. 示例代码

   ```c++
   #include <iostream>
   #include <string>
   #include <boost/json.hpp>
   using namespace std;
   int main()
   {
   	const char* json = "{\"name\":\"nash\",\"age\":35,\"args\":{\"cmd\":\"query\",\"params\":\"wzc\"}}";
   	boost::json::error_code  ec;
   	boost::json::value obj = boost::json::parse(json, ec);
   	if (ec) // 检查JSON 解析是否失败
   	{
   		std::cout << "Parsing failed: " << ec.message() << "\n";
   	}
   	
   	boost::json::value name = obj.as_object()["name"];
   	boost::json::value age  = obj.as_object()["age"];
   	
   	if (name.is_null()) // 判断对象的key是否存在
   	{
   		std::cout << "_++" << std::endl;
   	}
   	
   	// 获取值
   	// boost::json::string 要如下赋值
   	if(name.is_string())
   	{
   		boost::json::string tmp = name.as_string();
   		std::string std_name(tmp.begin(), tmp.end());
   		std::cout << "---" << std::endl;
   	}
   	
   	// Number 可以直接赋值给系统类型
   	if (age.is_number())
   	{
   		int _age = age.as_int64();
   		std::cout << "---" << std::endl;
   	}
   	
   	// 将一部分value 转换为string
   	boost::json::value args = obj.as_object()["args"];
   	if (args.is_object())
   	{
   		std::string str = boost::json::serialize(args);
   		std::cout << "str json: " << str << std::endl;
   	}
   	
   	
   	// 构造JSON-- 第一种方法
   	std::string private_ip = "172.18.80.183";
   	int count = 189;
   	boost::json::value jv = { 
   		{"cmd" , "vm_started"},
   		{"args", {
   			{"private_ip", private_ip},
   			{"name", "nash"},
   			{"paused", true},
   			{"count", count}
   			}
   		}
   	};
   	
   	std::string jvJSON = boost::json::serialize(jv);
   	std::cout << jvJSON << std::endl;
   	
   	
   	// 构造JSON-- 第二种方法
   	{
   		boost::json::object obj;                                        // construct an empty object
   		obj["pi"] = 3.141;                                              // insert a double
   		obj["happy"] = true;                                            // insert a bool
   		obj["name"] = "Boost";                                          // insert a string
   		obj["nothing"] = nullptr;                                       // insert a null
   		obj["answer"].emplace_object()["everything"] = 42;              // insert an object with 1 element
   		obj["list"] = { 1, 0, 2 };                                      // insert an array with 3 elements
   		obj["object"] = { { "currency", "USD" }, { "value", 42.99 } };  // insert an object with 2 elements
   		std::string jvJSON = boost::json::serialize(obj);
   		std::cout << jvJSON << std::endl;
   	}
   
   	return 0 ;
   }
   ```

4. 构建json

   ```c++
   // 这是推荐的做法
   int main()
   {
   	std::string name		= "nash";
   	std::string private_ip	= "172.18.80.183";
   	
   	
   	boost::json::object args;
   	args["private_ip"]	= private_ip;
   	args["name"]		= name;
   	
   	boost::json::array persons;
   	for (int i = 1; i < 5; i++) {
   		boost::json::object p;
   		p["age"] = i;
   		p["salary"] = i * 10;
   		persons.push_back(p);
   	}
   	
   	boost::json::object obj;
   	obj["cmd"]	= "vm_restart";
   	obj["args"] = args;
   	obj["person"] = persons;
   	
   	std::string message = boost::json::serialize(obj);
   	std::cout << message << std::endl;
   	return 0;
   }
   ```

   



# 第三章 日志

1. 示例代码

   ```c++
   // 告诉BOOST 动态链接
   // 链接的动态库 pthread boost_log_setup boost_log
   #define BOOST_LOG_DYN_LINK
   #include <boost/log/core.hpp>
   #include <boost/log/trivial.hpp>
   #include <boost/log/expressions.hpp>
   
   void init()
   {
   	boost::log::core::get()->set_filter
   	(
   	    boost::log::trivial::severity >= boost::log::trivial::info
   	);
   }
   
   int main(int, char*[])
   {
   	init();
   	BOOST_LOG_TRIVIAL(trace) << "A trace severity message";
   	BOOST_LOG_TRIVIAL(debug) << "A debug severity message";
   	BOOST_LOG_TRIVIAL(info) << "An informational severity message";
   	BOOST_LOG_TRIVIAL(warning) << "A warning severity message";
   	BOOST_LOG_TRIVIAL(error) << "An error severity message";
   	BOOST_LOG_TRIVIAL(fatal) << "A fatal severity message";
   
   	return 0;
   }
   ```
   
2. 封装

   ```cpp
   // LogHelper.h
   
   #pragma once
   #define BOOST_LOG_DYN_LINK
   #include <boost/format.hpp>
   #include <iostream>
   
   #include <boost/log/core.hpp>
   #include <boost/log/trivial.hpp>
   #include <boost/log/expressions.hpp>
   #include <boost/serialization/singleton.hpp>
   
   // 单例
   class LogHelper : public boost::serialization::singleton<LogHelper>
   {
   public:
   	LogHelper();
   	~LogHelper();
   
   	void trace(const std::string& input);
   	void debug(const std::string& input);
   	void info(const std::string& input);
   	void warning(const std::string& input);
   	void error(const std::string& input);
   	void fatal(const std::string& input);
   	
   	void init()
   	{
   		namespace logging = boost::log;
   		logging::core::get()->set_filter
   		(
   		    logging::trivial::severity >= logging::trivial::trace
   		);
   	}
   };
   
   
   #define LOG_TRACE	LogHelper::get_mutable_instance().trace
   #define LOG_DEBUG	LogHelper::get_mutable_instance().debug
   #define LOG_INFO	LogHelper::get_mutable_instance().info
   #define LOG_WARNING LogHelper::get_mutable_instance().warning
   #define LOG_ERROR	LogHelper::get_mutable_instance().error
   #define LOG_FATAL	LogHelper::get_mutable_instance().fatal
   
   ```

   ```cpp
   // LogHelper.cpp
   
   #include "LogHelper.h"
   
   LogHelper::LogHelper() {
   	this->init();
   }
   LogHelper::~LogHelper() {
   }
   
   void LogHelper::trace(const std::string& input)
   {
   	BOOST_LOG_TRIVIAL(trace) << input;
   }
   void LogHelper::debug(const std::string& input)
   {
   	BOOST_LOG_TRIVIAL(debug) << input;
   }
   void LogHelper::info(const std::string& input) 
   {
   	BOOST_LOG_TRIVIAL(info) << input;
   }
   void LogHelper::warning(const std::string& input)
   {
   	BOOST_LOG_TRIVIAL(warning) << input;
   }
   void LogHelper::error(const std::string& input)
   {
   	BOOST_LOG_TRIVIAL(error) << input;
   }
   void LogHelper::fatal(const std::string& input)
   {
   	BOOST_LOG_TRIVIAL(fatal) << input;
   }
   ```

   ```cpp
   // main.cpp
   
   #include <boost/lexical_cast.hpp>
   #include <iostream>
   #include <string>
   #include <boost/config.hpp>
   #include <boost/current_function.hpp>
   
   #include "LogHelper.h"
   int main()
   {
   	// 行号
   	std::string lineNum = BOOST_STRINGIZE(__LINE__);
   	std::cout << lineNum << std::endl;
   	
   	// 函数名
   	std::string str = BOOST_CURRENT_FUNCTION;
   	std::cout << "cur func : " << str << std::endl;
   	
   	//[函数名:行号] 内容(使用boost::format 来格式化即可)
   	LOG_TRACE("this is trace msg");
   	LOG_DEBUG("this is debug msg");
   	LOG_INFO("this is info msg");
   	LOG_WARNING("this is warning msg");
   	LOG_ERROR("this is error msg");
   	LOG_FATAL("this is fata msg");
   	return 0;
   }
   ```

   



# 第四章  Lock-free



## 4.1 无锁队列



### 4.1.1 queue

***





### 4.1.2 spsc_queue

***





## 4.2 无锁栈



### 4.2.1 stack







# 第五章 部署

1. 使用docker
2. 使用动态库，确保不能同时存在多个版本
3. 确保运行时的动态库和开发的版本一致