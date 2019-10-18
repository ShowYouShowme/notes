1. 传入参数

   ```shell
   # 方法一
   gdb ./test -args 111 222
   
   # 方法二
   # 在GDB环境中用set args
   (gdb) set args 111 222 333
   ```

2. 设置断点

   ```shell
   # 函数设置断点
   b OuterFactoryImp::readRedisDescConfig
   
   # 指定行设置断点
   b 515
   
   # 删除断点
   clear 515 # 515是行数
   delete breakpoints ${num}：# 删除第num个断点,简写d
   # 查看断点
   info breakpoints
   
   ```

3. 附加进程调试

   31. `gdb attach ${pid}`
   32. b HelloServantImp::testHello
   33. c

   
   
   
   
   
   
   
   
4. 错误信息
   
   ```shell
   # 原因：进程被框架杀死
   
   Warning:
   Cannot insert breakpoint 1.
   Error accessing memory address 0x40da64: Input/output error.
   Cannot insert breakpoint -71.
   Temporarily disabling shared library breakpoints:
   breakpoint #-71
   breakpoint #-70
   breakpoint #-72
   breakpoint #-1
   breakpoint #-2
   breakpoint #-69
   breakpoint #-10
   breakpoint #-13
   breakpoint #-15
   ```
   
   
   
   

