# 使用CLion远程调试Linux项目

1. centOS上安装gdbserver

   ```shell
   yum install gdb-gdbserver
   ```

2. 配置CLion![](img\微信截图_20190903105535.png)

   ![](D:\notes\工作笔记\艾文哲思\img\微信截图_20190903105713.png)

   ![(img\微信截图_20190903105823.png)

3. 启动gdbserver

   ```shell
   # 启动的方式调试
   gdbserver localhost:2334 ./gdb_remote ${arg1} ${arg2} ${arg3}
   
   # attach的方式调试
   gdbserver localhost:2334 --attach ${pid}
   
   # 注意 编译时优化等级为0且加参数-g
   ```

4. 启动CLion![](img\微信截图_20190903105823.png)