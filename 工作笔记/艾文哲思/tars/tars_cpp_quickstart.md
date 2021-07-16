# 服务命名

服务名称组成：

App：应用名

Server：服务名，提供服务的进程名称

Servant：服务者，提供服务的接口或实例

一个Server可以包含多个Servant，系统会使用服务的App + Server + Servant，进行组合，来定义服务在系统中的路由名称，称为路由Obj，其名称在整个系统中必须是唯一的，以便在对外服务时，能唯一标识自身。



# 服务开发

### 生成代码

```shell
1.修改`/root/Tars/cpp/servant/script/create_tars_server.sh`中`DEMO_PATH`为`/root/Tars/cpp/servant/script/demo`
2. chmod u+x  /root/Tars/cpp/servant/script/create_tars_server.sh
3. /root/Tars/cpp/servant/script/create_tars_server.sh TestApp HelloServer Hello
```

### 定义tars接口文件

参见tars_tup.md



### 服务编译

```shell
make cleanall
make	
make tar
#编译出现以下提示正常，因为Hello.h文件是动态生成的
HelloImp.h:5:19: fatal error: Hello.h: No such file or directory
 #include "Hello.h"
```



## 创建服务

## 服务编译

进入代码目录：

```shell
make cleanall
make	
make tar
```

## 扩展功能

如何增加新的接口

用`/usr/local/tars/cpp/tools/tars2cpp`生成对应的头文件

 ## 客户端调用服务器



