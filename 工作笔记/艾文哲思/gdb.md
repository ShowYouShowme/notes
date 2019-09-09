1. 传入参数

   ```shell
   # 方法一
   gdb ./test -args 111 222
   
   # 方法二
   # 在GDB环境中用set args
   (gdb) set args 111 222 333
   ```

2. 断点

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

   

