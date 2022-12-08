# 第一章 安装

1. 下载代码

   ```shell
   wget -e "https_proxy=http://192.168.0.101:8090" https://github.com/protocolbuffers/protobuf/archive/v3.9.0-rc1.tar.gz
   ```

2. 编译安装

   ```shell
   #~/.bashrc 里面配置环境变量
   #export C_INCLUDE_PATH=$HOME/usr/include/
   #export CPLUS_INCLUDE_PATH=$HOME/usr/include/
   #export LD_LIBRARY_PATH=$HOME/usr/lib/
   #export LIBRARY_PATH=$HOME/usr/lib/
   
   tar -zxvf v3.9.0-rc1.tar.gz
   cd ./protobuf-3.9.0-rc1/
   yum install -y libtool automake autoconf curl make unzip gcc-c++   
   ./autogen.sh
   ./configure --prefix=$HOME/usr
   make -j${CPU核心}  # top命令然后按数字1即可显示CPU核心数
   make install
   ```
   

# 第二章 使用教程



## 2.1 第一个例子

***

1. 演示代码

   ```cpp
   #include <iostream>
   #include <string>
   #include "person.pb.h"
   
   using namespace std;
   
   int main(int argc, char* argv[])
   {
   	GOOGLE_PROTOBUF_VERIFY_VERSION;
   
   	tutorial::Person person;
   
   	//将数据写到person.pb文件
   	person.set_id(123456);
   	person.set_name("Mark");
   	person.set_email("mark@example.com");
   
   	string out;
   	person.SerializeToString(&out);
   
   
   	//从person.pb文件读取数据
   	tutorial::Person new_person;
   	if (!new_person.ParseFromString(out)) {
   		cerr << "Failed to parse person.pb." << endl;
   		exit(1);
   	}
   
   	cout << "ID: " << new_person.id() << endl;
   	cout << "name: " << new_person.name() << endl;
   
   	getchar();
   	return 0;
   }
   ```

2. proto文件

   ```protobuf
   syntax = "proto3";
   package tutorial;
   message Person {
     int32 id = 1;
     string name = 2;
     string email = 3;
   }
   ```

3. 将proto文件生成C++源文件

   ```shell
   protoc --cpp_out=./ person.proto
   ```
   
4. makefile

   ```makefile
   # 链接的库要加上pthread,否则会报错
   main:main.cpp person.pb.cc
           g++  -std=c++11 main.cpp person.pb.cc -o main -lprotobuf -lpthread
   ```



## 2.2 高级

***

### 2.2.1 Proto文件

```protobuf
syntax = "proto3";
package tutorial;
message Goods
{
	int32 id = 1;
	int32 count = 2;
}
message Person {
  int32 id = 1;
  string name = 2;
  string email = 3;

  repeated string friendNames = 4;
	map<int32, int32> salary = 5;
	Goods		goods = 6;

	repeated Goods table = 7;
	map<int32, Goods> mg = 8;
}
```

### 2.2.2 成员是基本类型

1. 集合类型

   11. repeated 类型

       ```c++
       // 插入数据
       person.add_friendnames("Nash Jonh");
       // 遍历数据
       for (size_t i = 0; i < new_person.friendnames_size(); ++i)
       {
           string name = new_person.friendnames(i);
           cout << "name : " << name << endl;
       }
       ```

   12. map类型

       ```c++
       //插入数据
       auto ptr = person.mutable_salary();
       for (size_t i = 1; i < 15; ++i)
       {
           (*ptr)[i] = i * i;
       }
       
       //遍历数据
       for (auto it = new_person.salary().begin(); it != new_person.salary().end(); ++it)
       {
           int key = it->first;
           int value = it->second;
           cout << it->first << " : " << it->second << endl;
       }
       ```

       

2. 非集合类型

   ```c++
   // 读
   cout << "ID: " << new_person.id() << endl;
   
   // 写
   person.set_id(123456);
   ```

   

### 2.2.2 成员是自定义类型

1. 集合类型

   11. repeated类型

       ```c++
       // 写
       auto ptr = person.add_table();
       ptr->set_count(11);
       ptr->set_id(22);
       
       ptr = person.add_table();
       ptr->set_count(33);
       ptr->set_id(44);
       
       
       // 读
       auto& table = person.table();
       for (auto it = table.begin(); it != table.end(); ++it)
       {
           cout << it->count() << " : " << it->id() << endl;
       }
       ```

   12. map类型

       ```c++
       // 写
       auto mg = person.mutable_mg();
       tutorial::Goods goods;
       goods.set_count(999);
       goods.set_id(888);
       (*mg)[128] = goods;
       
       
       goods.set_count(666);
       goods.set_id(777);
       (*mg)[512] = goods;
       
       
       // 读
       auto& mg = person.mg();
       for (auto it = mg.begin(); it != mg.end(); ++it)
       {
           cout << "key : " << it->first << ", value : " << it->second.count() << " : " << it->second.id() << endl;
       }
       ```

       

2. 非集合类型

   ```c++
   // 写
   auto ptr = person.mutable_goods();
   ptr->set_count(96);
   ptr->set_id(156);
   
   // 读
   auto& goods = new_person.goods();
   cout << goods.count() << " : " << goods.id() << endl;
   ```

   
