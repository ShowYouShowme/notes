# 一、设置Visual C++布局



## 1.1 导入和导出设置

![](img/vs-1.png)

## 1.2 重置所有设置

![](img/vs-2.png)

## 1.3 仅重置设置

![](img/vs-3.png)

## 1.4 Visual C++

![](img/vs-4.png)



# 二、远程调试Linux项目



## 2.1  Linux挂载win文件夹



## 2.2 将开源代码解压至共享目录

![](D:\notes\记忆文件夹\img\vs-d-1.png)





## 2.3 vs创建Linux项目，导入项目

![](D:\notes\记忆文件夹\img\vs-d-2.png)



## 2.4 配置在Linux下编译

![](D:\notes\记忆文件夹\img\vs-d-3.png)



## 2.5 配置源文件路径

![](D:\notes\记忆文件夹\img\vs-d-4.png)



## 2.6 设置文件夹映射

![](D:\notes\记忆文件夹\img\vs-d-5.png)





## 2.7 配置构建和调试

![](D:\notes\记忆文件夹\img\vs-d-6.png)





## 2.8 构建项目

![](D:\notes\记忆文件夹\img\vs-d-7.png)



## 2.9 配置调试信息

![](D:\notes\记忆文件夹\img\vs-d-8.png)





## 2.10 断点调试

1. 在源文件里打断点
2. 点击<b style="color:red">本地Windows调试器</b>来单步调试



## 2.11 注意

1. 编译时必须加上`-g`选项，然后关闭优化

2. 查看程序是否有调试信息，如果没有调试信息，vs里显示<b style="color:red">不会命中断点</b>

   ```shell
   gdb ./stunserver
   
   # 如果有调试信息,显示如下
   Reading symbols from /root/stunserver/stunserver...done.
   
   # 没有调试信息,显示如下
   Reading symbols from /root/stunserver/stunserver...(no debugging symbols found)...done.
   ```

   