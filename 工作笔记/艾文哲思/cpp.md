# 可变模板参数

```c++
template<typename T>
std::string toString(T t){
	ostringstream os;
	os << t;
	return os.str();
}
template<typename T, typename... Args>
std::string toString(T head, Args... args){
	ostringstream os;
	os << head;
	return os.str() + toString(args...);
}
int main(){
	std::string s1 = toString(12, "ABC", 12.5, true);
	std::cout << s1 << std::endl;
	return 0;
}
```



# 获取日期

```cpp
static std::string DatetimeToString(time_t time)
{
	tm *tm_ = localtime(&time);                // 将time_t格式转换为tm结构体
	int year, month, day;// 定义时间的各个int临时变量。
	year = tm_->tm_year + 1900;                // 临时变量，年，由于tm结构体存储的是从1900年开始的时间，所以临时变量int为tm_year加上1900。
	month = tm_->tm_mon + 1;                   // 临时变量，月，由于tm结构体的月份存储范围为0-11，所以临时变量int为tm_mon加上1。
	day = tm_->tm_mday;                        // 临时变量，日。

	int hour = tm_->tm_hour;
	int minute = tm_->tm_min;
	int second = tm_->tm_sec;

	std::ostringstream os;
	os << year << "-"  
	   << std::setw(2) << std::setfill('0') << month << "-"  
	   << std::setw(2) << std::setfill('0') << day << " "
	   << std::setw(2) << std::setfill('0') << hour << ":"  
	   << std::setw(2) << std::setfill('0') << minute << ":"  
	   << std::setw(2) << std::setfill('0') << second;
	std::string date = os.str();
	return date;                                // 返回转换日期时间后的string变量。
}
```



# 指定长度数据类型

```c++
#include <stdint.h>
int main()
{
	int8_t a1		= INT8_MIN;
	int8_t a2		= INT8_MAX;

	int16_t b1		= INT16_MIN;
	int16_t b2		= INT16_MAX;

	int32_t c1		= INT32_MIN;
	int32_t c2		= INT32_MAX;

	int64_t d1		= INT64_MIN;
	int64_t d2		= INT64_MAX;

	uint8_t aa1		= UINT8_MAX;
	uint16_t bb1	= UINT16_MAX;
	uint32_t cc1	= UINT32_MAX;
	uint64_t dd1	= UINT64_MAX;
	return 0;
}
```



# 宏定义

```c++
// A(m) 展开为 'm' 
#define A(x)　　#@x

// B(m) 展开为 "m"
#define B(x)　　#x

// C(List) 展开为 ClassList
#define C(x)　　Class##x
```



# 异步编程

[异步编程](https://www.cnblogs.com/moodlxs/p/10111601.html)





# 全局变量与类的静态成员变量

1. 用**函数返回静态局部变量**替代全局变量
2. 用静态成员函数返回静态局部变量替代静态成员变量





# 匿名空间


用匿名空间函数替代静态全局函数。隐藏实现。
作用：符号仅在本编译单元可见。在cpp里面匿名空间里定义符号，比如全局变量，全局函数，类，枚举等，不会与其它cpp的符号重定义




# 占位符替换字符串

```c++
namespace
{
	// 占位符替换,类似Python
	//Usage :	auto t = formatString("INSERT INTO {0} WHERE `id` = {1}, `value` = {0}, `name` = {2}", toStringVec(111, 999, "wzc"));
	std::vector<std::string> subsVec;
	std::string formatString(std::string target, const std::vector<std::string>& subs) {
		for (size_t i = 0; i < subs.size(); ++i) {
			std::string placeholders = "{" + std::to_string(i) + "}";
			const std::string& sub = subs.at(i);
			size_t pos = target.find(placeholders);
			size_t placeholders_len = placeholders.length();
			while (pos != std::string::npos) {
				target.replace(pos, placeholders_len, sub);
				pos = target.find(placeholders);
			}
		}
		return target;
	}

	template<typename T>
	std::vector<std::string> toStringVec(T t) {
		ostringstream os;
		os << t;
		subsVec.push_back(os.str());
		std::vector<std::string> result = subsVec;
		subsVec.clear();
		return result;
	}
	template<typename T, typename... Args>
	std::vector<std::string> toStringVec(T head, Args... args) {
		ostringstream os;
		os << head;
		subsVec.push_back(os.str());
		return toStringVec(args...);
	}
}
```




# JSON

## map打印为JSON

```c++
template<typename T>
std::string mToString(const T& param)
{
	ostringstream os;
	os << param;
	return os.str();
}

template<>
std::string mToString<std::string>(const std::string& param)
{
	ostringstream os;
	os << "\"" << param << "\"";
	return os.str();
}
template<typename Key, typename Value>
std::string mToString(const map<Key, Value>& param)
{
	ostringstream os;
	os << "{";
	size_t len = param.size();
	size_t idx = 0;
	for (auto& elem : param) {
		os << "\"" << elem.first << "\":" << mToString(elem.second);
		if (idx != len - 1) {
			os << ",";
		}
		idx += 1;
	}
	os << "}";
	return os.str();
}
```



## Vector转换为JSON

```c++
template<typename Value>
std::string VectorToString(const Value& param)
{
	ostringstream os;
	os << param;
	return os.str();
}

template<>
std::string VectorToString<std::string>(const std::string& param)
{
	ostringstream os;
	os << "\"" << param << "\"";
	return os.str();
}

template<typename Value>
std::string VectorToString(const std::vector<Value>& param)
{
	ostringstream os;
	os << "[";
	size_t len = param.size();
	size_t idx = 0;
	for (auto& elem : param) {
		os << VectorToString(elem);
		if (idx != len - 1) {
			os << ",";
		}
		idx += 1;
	}
	os << "]";
	return os.str();
}

struct Company
{
	std::string address;
	int			phone;
};

template<>
std::string VectorToString<Company>(const Company& param)
{
	ostringstream os;
	os << "{";
	os << "\"" << "address" << "\":";
	os << param.address << ",";
	os << "\"" << "phone" << "\":";
	os << param.phone;
	os << "}";
	return os.str();
}
```

测试代码

```c++
int main()
{

	std::vector<int> v1 = { 1, 2, 3, 4, 5, 6, 7 };
	auto s1 = VectorToString(v1);
	std:vector<std::string> v2 = { "11","222","555","990" };
	auto s2 = VectorToString(v2);
	std::vector<Company> v3 = {
		{
			"北京中关村", 8619223
		},
		{
			"深圳南山科技园", 129334
		},
		{
			"深圳坂田", 8888434
		}
	};
	auto ss = VectorToString(v3);
	return 0;
}
```



# 常见报错信息

1. 模板报错

   > + 查看实例化时传入的模板参数类型
   > + 找不到匹配的函数，会试图类型转换，然后转换失败





# 去除变量未使用的警告

```c++
int a = 127;
(void)a; // 去除警告
```

# 智能指针包装对象

+ 关键点

  > 1. 构造函数设置为私有
  > 2. 用静态Create函数返回包装后的指针

+ 代码

  ```c++
  class Cup
  {
  private:
  	std::string name;
  	std::string color;
  	Cup(){
  		std::cout << "construct a Cup object!" << std::endl;
  	}
  public:
  	static std::shared_ptr<Cup> Create()
  	{
  		return std::shared_ptr<Cup>(new Cup());
  	}
  	~Cup()
  	{
  		std::cout << "delete a Cup Object" << std::endl;
  	}
  };
  
  int main()
  {
  	auto p1 = Cup::Create();
  	auto p2 = Cup::Create();
  	p2 = p1;
  	return 0;
  }
  ```



# 前置声明

1. 类的前置声明

   ```c++
   class Person;
   struct App;
   ```

2. 枚举的前置声明

   ```C++
   enum Region : int;
   ```

3. 命名空间里的类的前置声明

   ```c++
   namespace tars
   {
       class Application;
   }
   ```





