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

  