# 功能

一键编译、copy和重启服务



# 使用方法

1. 在makefile里面添加下面的代码

   ```makefile
   all1:
           @make cleanall
           @make -j4
           @bash ./complie_copy_reboot.sh
   ```

2. 把*complie_copy_reboot.sh*放到项目根目录

3. make all1