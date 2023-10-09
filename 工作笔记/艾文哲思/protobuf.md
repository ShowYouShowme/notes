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

   



## 2.3 常见语法

```ini
[package]
desc = 用于避免命名冲突的，会生成命名空间，比如C++语言，go语言里没用

[go_package]
desc = package名，生成的代码会存放在${go_package}文件夹里面;go语言专用

[syntax]
desc = proto版本，可选的值是proto2 或者 proto3

[import]
desc = 导入变量
```



示例

```protobuf
// person.proto
syntax = "proto3";
package witeHouse;  // go 语言不需要,c++ 里是命名空间名称
option go_package="/witeHouse"; // go语言必须加这行,分号前是生成文件路径;后面是package名称
import "common.proto";
message all_person {    //  aa_bb 会生成 AaBb 的驼峰命名的结构体
  repeated person Per = 1;
}
```



必须先编译common.proto，然后再编译person.proto，最后才能在代码里面使用





# 第三章 golang项目规范



## 3.1 代码结构

```shell
rummy
|
|------netMessage
|
|------proto
|
|------main.go
```



## 3.2 说明

1. netMessage 里面存放pb生成的文件和grpc文件
2. proto里面存放定义的proto文件
3. proto里面全部文件的option go_package="/netMessage";



## 3.3 生成的命令

```shell
# 生成ProtoBuf,  /proto 目录执行
protoc --go_out=..\  .\message.proto

# /proto 目录执行
protoc --go_out=..\  --go-grpc_out=..\ .\cmd.proto
protoc --go_out=..\  --go-grpc_out=..\ .\gateway.proto
protoc --go_out=..\  --go-grpc_out=..\ .\rummy.proto
```



## 3.4 proto文件

1. cmd.proto

   ```protobuf
   syntax = "proto3";
   package cmd;
   option go_package ="/netMessage";
   
   // ServiceId 服务代码 固定为两位
   enum ServiceId {
     UNKNOWN = 0;
     SYS     = 10;
     BFF_API = 11;
     BFF_GM = 12;
     SERVICE_AUTH = 13;
     SERVICE_FINANCE = 14;
     SERVICE_AGENT = 15;
     SERVICE_HALL = 16;
     SERVICE_ACTIVITY = 17;
     SERVICE_RECORD = 18;
     GAME_RUMMY = 19;
     SERVICE_STADIUM = 20;
     SERVICE_COMPETITION = 21;
   }
   
   // 消息命令 固定为四位， 前两位固定为ServiceId，用于区别命令属于哪个服务
   // 客户端发送的命令前缀为C_，服务端发送的命令前缀为S_
   enum CMD {
     CMD_UNKNOWN = 0; // 未知消息
     C_SYS_PING  = 1001;
     S_SYS_PONG  = 1002;
     C_EXAMPLE = 1003;
     S_EXAMPLE = 1004;
   }
   ```

2. gateway.proto

   ```protobuf
   syntax = "proto3";
   
   import "cmd.proto";
   package gateway;
   option go_package ="/netMessage";
   
   
   // 网关服务
   service GatewayService {
     rpc PushMessage(PushMessageReq) returns (PushMessageResp); // 请求网关推送消息给客户端
   }
   
   // 推送消息req
   message PushMessageReq {
     int64 uid = 1;
     cmd.ServiceId serviceId = 2;
     cmd.CMD cmd = 3;
     bytes data = 4;
   }
   
   // 推送消息resp
   message PushMessageResp {
   }
   ```

3. rummy.proto

   ```protobuf
   syntax = "proto3";
   import "cmd.proto";
   import "gateway.proto";
   package rummy;
   option go_package="/netMessage";
   
   message EnterGameReq{
   
   }
   
   message EnterGameResp{
   
   }
   
   message OnMessageReq {
     int64 uid = 1;
     int32 sid = 2;
     cmd.CMD cmd = 3;
     bytes data = 4;
   }
   
   message OnMessageResp {
   }
   ```

   
