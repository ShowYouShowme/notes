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

// 快速抛出异常
#define THROW_LOGIC_ERROR(...) toString("[", __FILE__, ":" , __LINE__ , ":" , __FUNCTION__ , "] ", __VA_ARGS__)
int main(){
	std::string s1 = toString(12, "ABC", 12.5, true);
	std::cout << s1 << std::endl;
	return 0;
}
```

利用引用传出参数

```cpp
template<typename T1, typename T2, typename T3>
void toString(string& out, T1 t1, T2 t2, T3 t3) {
	ostringstream os;
	os << t1 << ":" << t2 << ":" << t3;
	out += os.str();
}
template<typename T1, typename T2, typename T3,typename... Args>
void toString(string& out, T1 t1, T2 t2, T3 t3, Args... args) {
	ostringstream os;
	os << t1 << ":" << t2 << ":" << t3 << ":";
	out += os.str();
	toString(out, args...);
}
```



# 简化map插入元素

```c++
template<typename T>
void mapInsert(T& m, const typename T::key_type& key, const typename T::mapped_type& value)
{
	m.insert(make_pair(key, value));
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

1. **std::async**

   ```cpp
   #include <future>
   #include <iostream>
   using namespace std;
   
   
   bool is_prime(int x)
   {
   	for (int i = 1; i < x; i++)
   	{
   		int b = x / i;
   	}
   	return true;
   }
   
   
   int main()
   {
       // 调用函数is_prime,不等其结束直接返回
   	std::future<bool> fut = std::async(is_prime, 700020007);
   	std::cout << "please wait";
   	std::chrono::milliseconds span(100);
       
       // 等待返回结果,100毫秒超时
   	while (fut.wait_for(span) != std::future_status::ready)
   		std::cout << ".";
   	std::cout << std::endl;
   
   	bool ret = fut.get(); // 获取返回结果,如果函数尚未执行完毕,则阻塞
   	std::cout << "final result: " << ret << std::endl;
   	return 0;
   }
   ```

2. **std::future**：传递其它线程中操作的数据结果，是std::async、std::promise、std::packaged_task的底层对象。

3. **std::promise**：不同线程的同步机制

   ```cpp
   // promise example
   #include <iostream>       // std::cout
   #include <functional>     // std::ref
   #include <thread>         // std::thread
   #include <future>         // std::promise, std::future
   
   void print_int (std::future<int>& fut) {
     int x = fut.get(); // 此函数最多只能调用一次
     std::cout << "value: " << x << '\n';
   }
   
   int main ()
   {
     std::promise<int> prom;                      // create promise
   
     std::future<int> fut = prom.get_future();    // engagement with future
   
     std::thread th1 (print_int, std::ref(fut));  // send future to new thread
   
     prom.set_value (10);                         // fulfill promise
                                                  // (synchronizes with getting the future)
     th1.join();
     return 0;
   }
   ```

4. **std::packaged_task**：存储一个函数操作，并将其返回值传递给对应的future， 而这个future在另外一个线程中也可以安全的访问到这个值。

   ```cpp
   // packaged_task example
   #include <iostream>     // std::cout
   #include <future>       // std::packaged_task, std::future
   #include <chrono>       // std::chrono::seconds
   #include <thread>       // std::thread, std::this_thread::sleep_for
   
   // count down taking a second for each value:
   int countdown (int from, int to) {
     for (int i=from; i!=to; --i) {
       std::cout << i << '\n';
       std::this_thread::sleep_for(std::chrono::seconds(1));
     }
     std::cout << "Lift off!\n";
     return from-to;
   }
   
   int main ()
   {
     std::packaged_task<int(int,int)> tsk (countdown);   // set up packaged_task
     std::future<int> ret = tsk.get_future();            // get future
   
     std::thread th (std::move(tsk),10,0);   // spawn thread to count down from 10 to 0
   
     // ...
   
     int value = ret.get();                  // wait for the task to finish and get result
   
     std::cout << "The countdown lasted for " << value << " seconds.\n";
   
     th.join();
   
     return 0;
   }
   ```

   





# 全局变量与类的静态成员变量

1. 用**函数返回静态局部变量**替代全局变量
2. 用静态成员函数返回静态局部变量替代静态成员变量





# 匿名空间

用匿名空间函数替代静态全局函数和静态全局变量。隐藏实现。
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



# static

+ 符号前加static

  1. 静态全局变量：用匿名空间替换

     ```
     仅对当前编译单元，其他文件不可访问，其他文件可以定义与其同名的变量，两者互不影响.
     ```

  2. 静态全局函数：用匿名空间替换

     ```shell
     仅对当前编译单元，其他文件不可访问，其他文件可以定义与其同名的静态全局函数，两者互不影响.
     ```

  3. 静态成员函数

  4. 静态成员：不建议使用

     ```shell
     用静态成员函数返回静态局部变量替换
     ```

  5. 静态局部变量

+ 符号前不加static

  1. 全局函数：不建议使用

     ```
     可以在其它编译单元使用,使用前用extern声明
     ```

  2. 全局变量：不建议使用

     ```
     可以在其它编译单元使用,使用前用extern声明
     ```

     


# extern

+ 作用：导入符号，该符号在其它地方定义

+ 示例

  ```c++
  extern int num; // num 在其它编译单元定义
  
  extern void fun(); // 函数声明,该函数在其它地方定义
  
  // 符号不重整,CPP支持函数重载,因此编译的时候会重整符号,C语言则不会
  extern "C" {
  // ....
  }
  ```
  
+ extern "C"

  1. C语言编译生成的DLL，符号名称(变量/函数)不会重整，C++调用时要特殊处理

     ```cpp
     extern "C"
     {
     #include <lua.h>
     #include <lauxlib.h>
     #include <lualib.h>
     }
     ```

  2. C++编译生成的DLL，符号可以选择重整也可以不重整

     + 默认情况下符号会重整(支持函数重载)，C++调用直接包含**头文件**即可
     + 不重整符号[头文件用extern "C" 包含符号]，调用方式有以下几种
       1. 其它语言，比如python调用；只需要动态库，不需要头文件
       2. C++调用，依赖头文件，编译的时候链接
       3. C++调用，动态加载，不需要头文件

     

  



# 重定义

1. 多个cpp文件里有**同名的非static的全局变量**导致符号重定义
2. 多个cpp文件里有**同名的非static的全局函数**导致符号重定义
3. 不同cpp里面的同名class、struct和enum不会导致重定义，可以认为它们是static的
4. 同一个cpp里面多次定义class会导致重定义





# 内存访问错误

+ 原则

  > 1. 不操作裸指针,不能出现裸指针类型的变量和函数参数
  > 2. 不进行指针的运算，比如C语言里的+和-运算；&和*运算
  > 3. 尽可能不操作迭代器，非法迭代器的解引用会导致内存错误
  > 4. 分配内存(new,malloc之类)时可能会失败，记得判断返回值是否为NULL

+ 做法

  > 1. 访问vector的元素用at函数，越界会抛出异常
  > 2. 读取/修改map的元素用at元素，写入用insert函数
  > 3. 遍历容器用C++11的for迭代
  > 4. **使用STL的算法的时候，记得判断迭代器范围，非常容易越界**
  > 5. **STL算法仅操作STL的容器，不要操作C语言的数组之类的**
  > 6. 自定义类的对象用工厂方法创建，然后直接用智能指针包住；并且智能指针不提供获取裸指针api，智能指针可以判断是否为NULL；多线程安全
  
+ 智能指针使用规范

  ```cpp
  class Person
  {
  public:
  	static  shared_ptr<Person> Create(const string& name, int age){
  		try
  		{
  			return shared_ptr<Person>(new Person(name, age)); //C++ new分配内存失败,默认会抛出异常
  		}
  		catch (const std::bad_alloc& e)
  		{
  			std::cerr << "allocate failed!" << endl;
  			throw std::bad_alloc();
  		}
  	}
  	void toString()
  	{
  		cout << "age : " << _age << " name : " << _name << endl;
  	}
  private:
  	// 构造函数设为私有
  	Person(const string&name, int age) :_name(name), _age(age) {}
  private:
  	int _age;
  	string _name;
  };
  
  
  int main()
  {
  	// 允许对shared_ptr<Person> 的操作
  	// 1：operator->
  	// 2：拷贝构造
  	// 禁止其它类型的操作
  	shared_ptr<Person> ptr = Person::Create("wzc", 28);
  	ptr->toString(); // operator 1
  
  	shared_ptr<Person> p2(ptr); // operator 2
  	p2->toString();
  	return 0;
  }
  ```

  



​     

# 动态库和静态库

+ 动态库

  > 多个版本的动态库同时存在时，可能会错误加载了低版本的动态库，如果两个版本不兼容会报错或者是程序执行结果与预期不一致！比如安装了新软件包，该软件包更新了某个动态库，可能会导致依赖该动态库旧版本的程序不能执行。

+ 静态库

  > 编译的时候代码直接copy至可执行文件，运行时不依赖于库。不过可执行文件体积较大，而且编译时间比使用动态库长。但是建议使用静态库！！！

+ Linux安装动态库的步骤

  ```shell
  # STEP1 查找已存在的动态库
  find / -name "lib${soname}*"
  
  # STEP2 删除已存在的动态库 ==软链接也要删除
  rm -f `find / -name "lib${soname}*"`
  
  # STEP3 安装需要的动态库
  
  # 例子  删除已经存在的libcurl库
  rm -f `find / -name "libcurl*"`
  ```



# 常用dll

+ ld-linux.so

  > 加载动态链接库

+ libstdc++.so

  > gcc中C++的动态库

+ libc.so

  > Linux下标准的C库，Linux系统中最底层的API，几乎其它任何的运行库都要依赖它。逐渐被glibc取代



# 建议

1. 尽量不使用auto，影响代码可读性，尤其是在git上阅读的时候
2. 禁止使用C语言的类型转换，用C++的替换

   + static_cast：对应C语言的隐式类型转换，一般用这个就够了
   + reinterpret_cast：**不建议使用**
   + const_cast：删除变量的const属性，**不建议使用**
   + dynamic_cast：父类指针转换为子类指针
3. 拒绝自定义类的隐式类型转换，用成员函数
   + toString()
   + toInt()
   + toDouble()
   + 等等
4. 类的构造函数一律用explicit修饰，禁止其他类型隐士转换到该类
5. new时，必须判断返回值是否为null，因为内存不足时会分配失败，用null指针会导致crash
6. 自定义对象的创建一律用Create函数，该函数返回的指针用智能指针包含
   + 用指针指针包含前先判断是否为null，当然智能指针内部也会判断null
   + 智能指针对象无法取得裸指针
   + 智能指针无法reset指针类型
   + 智能指针必须保证线程安全
   + 智能指针类型只有-->函数，没有*函数；并且-->操作有NULL判断
7. 禁止使用指针相关的运算符
   + 取变量地址运算符&
   + 解引用运算符*：非法的地址会导致程序崩溃
   + +和-运算
8. 只有自定义的类型才能用智能指针表示，并且该类型不是仅仅存储数据；其它类型一律用非指针类型！





# 多线程
### 基本概念

***

1. 线程不安全

   > 多个线程同时读/写数据(全局变量、类静态成员变量和静态局部变量等)，导致运行结果和单线程不一致

2. 导致线程不安全的原因

   > 1. 多个线程同时访问全局变量
   > 2. 多个线程同时访问类的静态成员变量
   > 3. 多个线程同时访问函数的静态局部变量
   > 4. 线程A把局部变量的引用传入线程B，导致线程A和B可以同时访问A的局部变量



### 示例

***

```cpp
#include <stdio.h>
#include <pthread.h>

int count = 1;

void* run(void * arg1)
{
    int i = 0;
    while(1)
    {
        int val = count;
        i++;
        printf("count is %d  \n", count);
        count = val+1;
        if(5000 == i)
            break;
    }
}


int main()
{
    pthread_t tid1, tid2;
    
    // 线程t1 和 t2 同时访问全局变量count
    pthread_create(&tid1, NULL, run, NULL);
    pthread_create(&tid2, NULL, run, NULL);

    pthread_join(tid1, NULL);
    pthread_join(tid2, NULL);
    return 0;
}
```
### 多线程常用模型

***

1. <span style="color:violet;font-weight:bold">master-worker模型</span>

   > master-worker模型类似于任务分发策略，开启一个master线程接收任务，然后在master中根据任务的具体情况进行分发给其它worker子线程，然后由子线程处理任务。如需返回结果，则worker处理结束之后把处理结果返回给master

2. <span style="color:violet;font-weight:bold">生产者消费者模型</span>

   > 其核心是使用一个缓存来保存任务。开启一个/多个线程来生产任务，然后再开启一个/多个来从缓存中取出任务进行处理。这样的好处是任务的生成和处理分隔开，生产者不需要处理任务，只负责向生成任务然后保存到缓存。而消费者只需要从缓存中取出任务进行处理

3. actor模型

   > actor模型属于一种基于消息传递机制并行任务处理思想，它以消息的形式来进行线程间数据传输，避免了全局变量的使用，进而避免了数据同步错误的隐患。actor在接受到消息之后可以自己进行处理，也可以继续传递（分发）给其它actor进行处理。在使用actor模型的时候需要使用第三方Akka提供的框架。

4. fork&join模型

   > 模型包含递归思想和回溯思想，递归用来拆分任务，回溯用合并结果。 可以用来处理一些可以进行拆分的大任务。其主要是**把一个大任务逐级拆分为多个子任务，然后分别在子线程中执行，当每个子线程执行结束之后逐级回溯，返回结果进行汇总合并，最终得出想要的结果。**这里模拟一个摘苹果的场景：有100棵苹果树，每棵苹果树有10个苹果，现在要把他们摘下来。为了节约时间，规定每个线程最多只能摘10棵苹树以便于节约时间。各个线程摘完之后汇总计算总苹果树

5. future模型

   > Future是把结果放在将来获取，当前主线程并不急于获取处理结果。允许子线程先进行处理一段时间，处理结束之后就把结果保存下来，当主线程需要使用的时候再向子线程索取
   >
   > 示例代码：
   >
   > ```cpp
   > #include <future>
   > #include <iostream>
   > using namespace std;
   > 
   > 
   > bool is_prime(int x)
   > {
   > 	for (int i = 1; i < x; i++)
   > 	{
   > 		int b = x / i;
   > 	}
   > 	return true;
   > }
   > 
   > 
   > int main()
   > {
   > 	std::future<bool> fut = std::async(is_prime, 700020007);
   > 	std::cout << "please wait";
   > 	std::chrono::milliseconds span(100);
   > 	while (fut.wait_for(span) != std::future_status::ready)
   > 		std::cout << ".";
   > 	std::cout << std::endl;
   > 
   > 	bool ret = fut.get();
   > 	std::cout << "final result: " << ret << std::endl;
   > 	return 0;
   > }
   > ```



# 构造函数抛出异常

1. 后果：内存泄漏

2. 示例

   ```cpp
   #include <iostream>
   using namespace std;
   
   class A
   {
   public:
   	A() { cout << "in A constructor" << endl; }
   	~A() { cout << "in A destructor" << endl; }
   };
   
   class B
   {
   public:
   	unique_ptr<A> pA;
   	B():pA(new A)
   	{
   		cout << "in B constructor" << endl;
   		throw - 1;
   	}
   	~B()
   	{
   		cout << "in B destructor" << endl;
   	}
   };
   
   int main()
   {
   	try
   	{
   		B b;
   	}
   	catch (int)
   	{
   		cout << "catched" << endl;
   	}
   }
   ```

   运行结果

   ```shell
   in A constructor
   in B constructor
   in A destructor
   catched
   ```






# 动态加载dll

## 主程序

1. 代码

   ```cpp
   #include <dlfcn.h>
   extern "C"
   {  
       typedef void(*FunPtr)();
   }
   int main()
   {
       void* handle = dlopen("./libPerson.so", RTLD_NOW);
       
       FunPtr fun = (FunPtr)dlsym(handle, "printDesc");
       
       fun();
       return 0;
   }
   ```

2. 编译

   ```shell
   g++ -g ./main.cpp -ldl
   ```



## 动态库

1. Person.h

   ```cpp
   extern "C" void printDesc();
   ```

2. Person.cpp

   ```cpp
   #include"Person.h"
   #include<iostream>
   using namespace std;
   
   
   void printDesc()
   {
       for(int i = 0; i < 19; ++i){
           cout << "i = " << i << endl;
       }
       int a = 1;
       int b =2;
       int c =a +b;
       cout << "c = " << c << endl;
   }
   ```

3. 编译动态库

   ```shell
   g++ -g Person.cpp -fpic -shared -o libPerson.so
   ```

   



