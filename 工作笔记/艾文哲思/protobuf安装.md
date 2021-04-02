# windows 安装使用protobuf

1. 从github上下载代码

   ```shell
   wget https://github.com/protocolbuffers/protobuf/archive/v3.9.0-rc1.zip
   ```

2. 生成`protoc.exe`和静态库`libprotobufd.lib`

   ![](img\微信截图_20190912214430.png)

   ![](img\微信截图_20190912214626.png)重新configure

![](img\微信截图_20190912214823.png)

![](img\微信截图_20190912214949.png)

![](img\微信截图_20190912215121.png)

![](img\微信截图_20190912215616.png)

3. 把源码的src目录下的**google文件夹**拷贝出来，放到项目的include目录里面；把**protoc.exe**放到项目的bin目录，把**libprotobufd.lib**放到项目的lib目录

4. 设置项目的**附加包含目录**、**附加库目录**和**附加依赖项**。注意：项目如果是64位的那么CMake生成的VS项目也必须是64位的！

5. 代码生成指定用静态库

   ![](img\微信截图_20190912221904.png)



# 附录

1. 演示代码

   ```
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

   



# centOS下安装protobuf

1. 下载代码

   ```shell
   wget -e "https_proxy=http://192.168.0.101:8090" https://github.com/protocolbuffers/protobuf/archive/v3.9.0-rc1.tar.gz
   ```

2. 编译安装

   ```shell
   tar -zxvf v3.9.0-rc1.tar.gz
   cd ./protobuf-3.9.0-rc1/
   yum install -y libtool automake autoconf curl make unzip gcc-c++   
   ./autogen.sh
   ./configure --prefix=/usr/local/protobuf
   make -j${CPU核心}  # top命令然后按数字1即可显示CPU核心数
   make install
   # refresh shared library cache.
   ldcnfig
   ```

3. 设置环境变量

   ```shell
   vim  /etc/profile
   # (动态库搜索路径) 
   export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/usr/local/protobuf/lib
   # (静态库搜索路径) 
   export LIBRARY_PATH=$LIBRARY_PATH:/usr/local/protobuf/lib
   export PATH=$PATH:/usr/local/protobuf/bin
   echo "/usr/local/protobuf/lib" >> /etc/ld.so.conf
   ldconfig
   # 执行命令重新加载环境变量
   source /etc/profile
   
   # 查看版本
   protoc --version
   ```

4. makefile示例

   ```makefile
   # 链接的库要加上pthread,否则会报错
   main:main.cpp person.pb.cc
           g++  -std=c++11 main.cpp person.pb.cc -o main -I/usr/local/protobuf/include -lprotobuf -lpthread
   ```

5. 编译时指定路径；编译和安装完成后，把include和lib里面的内容copy到系统对应路径，然后ldconfig刷新缓存就能使用动态库了