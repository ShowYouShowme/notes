# GCC介绍

+ 名称：GNU Compiler Collection
+ 管理与维护：GNU项目
+ 对C/C++编译的控制
  1. 预处理：宏定义错误
  2. 编译：语法错误，函数没有返回
  3. 汇编
  4. 链接：找不到符号

# GCC参数讲解

+ 基本使用格式 

  ```makefile
  gcc main.c -o main
  
  gcc main.c
  
  gcc -c main.c #生成main.o
  
  gcc main.o -o main #生成可执行文件main
  
  gcc -E main.c >  main.e #预处理 先复制头文件然后进行宏替换,可用此方法查看宏代码
  
  gcc -S main.c #产生汇编代码main.s
  
  gcc -g main.c -o main # 生成debug版本的可执行文件
  ```

  

# GCC编译多文件

1. 创建目录test和Person

2. 在test里面创建main.cpp，Person里面创建Peron.h和Peron.cpp文件

3. 进入test目录`g++ main.cpp ../Person/Person.cpp -o main -I ../Person`

4. 代码

   ```c++
   //main.cpp 
   #include<iostream>
   #include"Person.h"
   using namespace std;
    
   int main(int argc, char* argv[])
   {
        Person person;
        cout << "test g++" << endl;
        return 1;
   }
   
   //Person.h
   class Person
   {
       public:
       Person();
   };
   
   //Person.cpp
   #include"Person.h"
   #include<iostream>
   using namespace std;
   Person::Person()
   {
       cout << "Create Person" << endl;
   }
   ```

   

# GCC静态编译

1. 安装依赖

   ```shell
   yum install libstdc++-static
   yum install glibc-static
   ```

2. 示例

   ```shell
   g++ main.cpp -o main
   ldd main #查看可执行文件依赖的库
   
   #静态编译
   g++ main.cpp -o main_static -static
   ldd main_static
   
   # 生成静态库
   ar r libtest.a a.o b.o c.o
   
   
   ## 生成静态库并静态编译链接
   
   ## step1:生成静态库
   g++ -c hello.cpp   # 生成目标文件
   ar r libhello.a hello.o # 目标文件打包为.a静态库文件
   
   ## step2:编译时连接静态库
   ### 方法1：
   g++ test.cpp -lhello -L. -static -o test
   ### 方法2：
   g++ test.cpp libhello.a -L. -o test_1
   
   
   # 注意:g++ 4.8.5 CentOS7中,可以直接使用-l${libName} -L${libPath} 来链接
   # 如果存在so,则链接so,否则链接.a;即此指令可以链接动态库和静态库
   ```



# 注意

1. -l${soName}动态库链接的是lib${soName}.so,不是lib${soName}.so.1之类的
2. -l${aName}静态库链接的是lib${soName}.a,不是lib${soName}.a.1之类的

# GCC动态库编译和调用

```shell
#生成动态库
g++ Person.cpp -fpic -shared -o libPerson.so # 注意动态库命名规则

#编译项目时引入动态库 大写L执行动态库路径 小写l指定库名称
g++ main.cpp  -o main -I ../Person/ -L ../Person -l Person
```

启动可执行程序失败：

1. 将用到的动态链接库拷贝到`/usr/lib`目录

2. 设置环境变量`LD_LIBRARY_PATH`

   ```shell
   export LD_LIBRARY_PATH=../Person
   ```
   
3. 利用ldconfig

   > 1. 将dll所在的目录写入文件`/etc/ld.so.conf`
   >
   >    ```shell
   >    echo "/usr/local/protobuf/lib" >> /etc/ld.so.conf
   >    ```
   >
   > 2. 执行命令`ldconfig`






# 其它选项

+ -Wno-deprecated ：不要警告使用已弃用的功能
+ -Wall：使用警告
+ -O${level}：优化，level为0时不优化。**注意：优化后调试会错乱**



# 相关命令

+ nm：查看可执行文件中的符号信息
+ strip：去掉可执行文件中的符号信息，减小文件体积