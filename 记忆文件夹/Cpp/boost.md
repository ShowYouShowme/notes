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

   