# Tars C++框架的服务线程

## 服务线程的组成

| 名称                 | 功能                                                     | 数目       |
| -------------------- | -------------------------------------------------------- | ---------- |
| 主线程               | 服务端初始化                                             | 1          |
| **网络线程**         | **服务端网络收发数据包**                                 | **可配置** |
| 管理端口业务逻辑线程 | 接受和处理用户自定义命令、服务关闭命令等                 | 1          |
| 时间辅助线程         | 定期计算时间，减少系统对gettimeofday的调用               | 1          |
| 滚动日志线程         | 本地的文件创建和日志写入                                 | 1          |
| 本地日志线程         | 负责日志的文件创建和日志写入                             | 1          |
| 远程日志线程         | 同步日志到远程                                           | 1          |
| **业务逻辑处理线程** | **处理用户业务逻辑，完成服务的主要功能**                 | **可配置** |
| **客户端网络线程**   | **管理对外服务链接、监听读写事件、网络读写**             | **可配置** |
| 统计属性上报线程     | 收集统计和属性信息，定时同步到stat和property             | 1          |
| **异步回调线程**     | **执行异步回调函数，客户端每个网络线程有自己的异步线程** | **可配置** |



## 线程数计算

实验场景：

> - 服务端配置1个ServantObj，其配置5个业务逻辑线程。

> - 服务端配置1个网络线程

> - 客户端配置2个网络线程

> - 异步回调线程设置为2个。

线程数：

7（固定数）+ 1(服务端网络线程数目) + 5（业务处理线程数目）+ 2(客户端网络线程数目) + 2（异步回调线程数目）* 2(客户端网络线程数目) = 19个线程。

## 改变线程数

能改变的线程数目的线程：

> + 服务端网络线程
> + 业务逻辑处理线程
> + 客户端网络线程
> + 异步回调处理线程



改变业务逻辑线程数：

在Tars管理平台配置Servant对象时，在“线程数”输入自己想要的线程



改变其它线程数：

在模版上修改，或者增加对应的服务私有模版







# Tars开发规范

## 命名规范

### 服务命名

### Namespace命名

namespace一般为业务名，比如：

```c++
namespace Comm
```

### class命名

```c++
class HelloWorldApp
```

### 方法命名

动词打头，然后跟上表示动作对象的名词。小写字母开头，后面每个单词首字母大写。

```c++
getNumber(); 

setNumber(); 
// 响应消息     
onProcess(); 

doAddFile();

// has 和 can代替bool型函数
hasFile();

canPrint();

sendMessage(); 
```

### 变量命名

小写字母开头,后面每个单词的首字母大写,一般为名词。

```c++
string userNo; //（手机号）
string station;//（省份）
string destNo;//（目的号码）
string srcNo;//（源号码）

const int NUMBER_OF_GIRLFRIENDS = 1024;//常亮
```



## Tars文件目录规范

+ tars文件原则上和相应的server放在一起
+ 每个server在开发机上建立/home/tarsproto/[namespace]/[server]子目录
+ 所有tars文件需要更新到/home/tarsproto下相应server的目录
+ **makefile里面运行make release会自动完成上面两步操作**
+ **使用其他server的tars文件时，需要到/home/tarsproto中使用，不能copy到本目录下**
+ tars的接口原则上只能增加，不能减少或修改





## makefile规范

### makefile使用原则

***

+ Makefile只能有一个Target

+ 需要包含其它库时，根据依赖关系include

  ```makefile
  include /home/tarsproto/TestApp/HelloServer/HelloServer.mk
  include /usr/local/tars/cpp/makefile/makefile.tars
  ```

### 模板解释

***

```makefile
#-----------------------------------------------------------------------

APP           := TestApp  #程序名字空间 
TARGET        := HelloServer #服务名
CONFIG        := HelloServer.conf #配置文件名称
STRIP_FLAG    := N
TARS2CPP_FLAG  :=

INCLUDE       +=  # 其它需要包含的路径
LIB           +=  # 需要的库

#-----------------------------------------------------------------------

include /home/tarsproto/TestApp/HelloServer/HelloServer.mk
include /usr/local/tars/cpp/makefile/makefile.tars
```

注意：

```shell
RELEASE_TARS：需要发布在/home/tarsproto/目录下面的tars文件，如果需要把自己.h也发布到/home/tarsproto则可以如下：
RELEASE_TARS += xxx.h
CONFIG：配置文件名称，后面可以增加自己需要的文件，调用make tar时也会把该文件包含到tar包中；
```

### 使用

***

```shell
make help #可以看到makefile所有使用功能。

make tar #生成发布文件

make release #copy tars文件到/home/tarsproto相应目录，并自动生成相关的mk文件

make clean #清除

make cleanall #清除所有
```



# Tars框架Future/Promise使用

tars2cpp工具生成的头文件里面的RPC接口一共有四种：

+ 同步sync方法
+ 异步async方法
+ Future/Promise方法
+ 协程coco方法



## Future/Promise适用什么场景

你想买房，然后通过微信联系中介A、B、C看看行情并询问一些信息，最后拿到所有的信息汇总后再评估。



常见做法：

+ **同步做法**：先微信询问A，等待A的回复，接着询问B，等待B的回复，最后询问C，等待C的回复
+ **异步做法**：先微信询问A，在等待A回复的同时，可以干干其他事情，等到A回复后再依次询问B，C；
+ **Future/Promise**：同时给A、B、C发消息询问，等待回复的同时干其他事情，一直到所有回复都响应



## Future/Promise代码例子

```c++
// 可以对比一下javascript的Promise，以及第三方库bluebird
//回调函数
void handleAll(const promise::Future<promise::Tuple<promise::Future<TestServantPrxCallbackPromise::PromisetestPtr>, 
                    promise::Future<TestServantPrxCallbackPromise::PromisetestPtr> > > &result)
{
    promise::Tuple<promise::Future<TestServantPrxCallbackPromise::PromisetestPtr>, promise::Future<TestServantPrxCallbackPromise::PromisetestPtr> > out = result.get();
 
    promise::Future<TestServantPrxCallbackPromise::PromisetestPtr> out1 = out.get<0>();
    const tars::TC_AutoPtr<TestServantPrxCallbackPromise::Promisetest> print1 = out1.get();
 
    promise::Future<TestServantPrxCallbackPromise::PromisetestPtr> out2 = out.get<1>();
    const tars::TC_AutoPtr<TestServantPrxCallbackPromise::Promisetest> print2 = out2.get();
 
    DEBUGLOG("handleAll:" << print1->_ret << "|" << print1->outStr << "|out2:" << print2->_ret << "|" << print2->outStr);
}
 
int main()
{
    map<string, string> ctx;
    TestServantPrx testPrx = Application::getCommunicator()->stringToProxy<TestServantPrx>("Test.TestServer.TestServant");
 
    promise::Future<TestServantPrxCallbackPromise::PromisetestPtr > result1 = testPrx->promise_async_EchoTest("manmanlu1", ctx);
    promise::Future<TestServantPrxCallbackPromise::PromisetestPtr > result2 = testPrx->promise_async_EchoTest("manmanlu2", ctx);
 
    promise::Future<promise::Tuple<promise::Future<TestServantPrxCallbackPromise::PromisetestPtr>, promise::Future<TestServantPrxCallbackPromise::PromisetestPtr> > > r =
        promise::whenAll(result1, result2);
    r.then(tars::TC_Bind(&handleAll));
 
    DEBUGLOG("Test Future-Promise done");
}
```



# tars支持protobuf 描述文件

现在有部分业务采用了protobuf协议；想要把这些业务迁移到tars



## 使用方法

### 准备proto文件

proto文件的语法是不限制的，你可以使用proto2或proto3； 但一定加上**option cc_generic_services=false**

```protobuf
syntax = "proto2";

option cc_generic_services=false;

package TestApp;

message PbRequest {
    required int32 a = 1;
    required int32 b = 2;
}

message PbResponse { 
    required int32 c = 1;
}  

service Hello {
    rpc add(PbRequest) returns (PbResponse) {
    }
}
```

### 直接执行make

