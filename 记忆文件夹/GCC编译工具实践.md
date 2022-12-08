# 第一章 GCC介绍

+ 名称：GNU Compiler Collection
+ 管理与维护：GNU项目
+ 对C/C++编译的控制
  1. 预处理：宏定义错误
  2. 编译：语法错误，函数没有返回
  3. 汇编
  4. 链接：找不到符号

# 第二章 GCC参数讲解

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

  

# 第三章 GCC编译多文件

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

   

# 第四章 GCC静态编译



## 4.1 安装依赖

***

```shell
yum install libstdc++-static
yum install glibc-static
```



## 4.2 示例

***

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



## 4.3 注意

***

1. -l${soName}动态库链接的是lib${soName}.so,不是lib${soName}.so.1之类的
2. -l${aName}静态库链接的是lib${soName}.a,不是lib${soName}.a.1之类的

# 第五章 GCC动态库编译和调用

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





# 第六章  其它



## 6.1 选项

***

+ -Wno-deprecated ：不要警告使用已弃用的功能
+ -Wall：使用警告
+ -O${level}：优化，level为0时不优化。**注意：优化后调试会错乱**



## 6.2 相关命令

***

+ nm：查看可执行文件中的符号信息
+ strip：去掉可执行文件中的符号信息，减小文件体积



## 6.3 make 相关

***

1. 多核心编译

   ```shell
   make -j${jobNum}
   
   #1
   不指定jobNum时,make不会限制使用的核心数,可能会用完全部cpu核心
   
   #2 
   多核心同时编译,会使用较大的内存,如果内存不足会导致编译失败,因此内存不足时可以将核心数设置为1
   make -j1
   ```




## 6.4 动态库符号查找

```shell
nm -D ${soName} | grep ${symbol}

nm -D libboost_stacktrace_addr2line.so.1.75.0 | grep dladdr
```





# 第七章 升级



## 7.1 使用devtoolset升级

***

### 1.1 升级到7.3

```shell
yum -y install centos-release-scl
yum -y install devtoolset-7-gcc devtoolset-7-gcc-c++ devtoolset-7-binutils

# scl命令启用只是临时的，退出shell或重启就会恢复原系统gcc版本
scl enable devtoolset-7 bash

# 长期使用
echo "source /opt/rh/devtoolset-7/enable" >>/etc/profile
```



### 1.2 升级到8.3

```shell
yum -y install centos-release-scl
yum -y install devtoolset-8-gcc devtoolset-8-gcc-c++ devtoolset-8-binutils
# scl命令启用只是临时的，退出shell或重启就会恢复原系统gcc版本
scl enable devtoolset-7 bash

# 长期使用
echo "source /opt/rh/devtoolset-8/enable" >>/etc/profile
```



### 1.3 升级到9.3

```shell
yum -y install centos-release-scl
yum -y install devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils
# scl命令启用只是临时的，退出shell或重启就会恢复原系统gcc版本
scl enable devtoolset-9 bash

# 长期使用
echo "source /opt/rh/devtoolset-9/enable" >>/etc/profile
```





## 7.2 使用Docker

***

C++ 的server 部署在Docker 里面可以确保环境一致，避免很多问题。这是非常推荐的做法。





# 第八章 搜索路径



## 8.1 环境变量

首先明确一点，这几个预处理包含目录的环境变量并不是Linux操作系统的一部分，因此一般情况下Linux是不会设置这些环境变量的。所以在对某一个环境变量第一次设置时，应该直接将其赋值为所需的目录，在之后的设置中再使用递归式的赋值。使用非root用户编译时，记得先创建$HOME/usr目录，然后      编译时配置--prefix=$HOME/usr

1. gcc头文件的搜索路径

   ```shell
   export C_INCLUDE_PATH=$HOME/usr/include/
   ```

2. g++头文件搜索路径

   ```shell
   export CPLUS_INCLUDE_PATH=$HOME/usr/include/
   ```

3. ***程序加载运行期间***查找动态链接库时，指定除了系统默认路径之外的其他路径，发布的时候使用

   ```shell
   export LD_LIBRARY_PATH=$HOME/usr/lib/
   ```

4. ***程序编译期间***查找动态链接库时指定查找共享库的路径，开发过程中使用

   ```shell
   export LIBRARY_PATH=$HOME/usr/lib/
   ```



## 8.2 做法

使用非root用户编译安装软件时，先创建目录$HOME/usr，然后把源码编译的软件安装到$HOME/usr，最后.bashrc 里面配置上面的四个环境变量，之后再编译其它的软件时就可以找到这些头文件和目录了，并且不会污染到其它的用户。然后make install 就不需要root用户的权限了。
