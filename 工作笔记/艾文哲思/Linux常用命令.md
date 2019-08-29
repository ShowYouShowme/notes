# netstat

1. 列出所有端口情况

   > ```shell
   > [root@xiesshavip002 ~]# netstat -a      # 列出所有端口
   > [root@xiesshavip002 ~]# netstat -at     # 列出所有TCP端口
   > [root@xiesshavip002 ~]# netstat -au     # 列出所有UDP端口
   > ```

2. 列出所有处于监听状态的 Sockets

   > ```shell
   > [root@xiesshavip002 ~]# netstat -l   # 只显示监听端口
   > [root@xiesshavip002 ~]# netstat -lt  # 显示监听TCP端口
   > [root@xiesshavip002 ~]# netstat -lu  # 显示监听UDP端口
   > [root@xiesshavip002 ~]# netstat -lx  # 显示监听UNIX端口
   > ```

3. 显示每个协议的统计信息

   > ```shell
   > [root@xiesshavip002 ~]# netstat -s     # 显示所有端口的统计信息
   > [root@xiesshavip002 ~]# netstat -st    # 显示所有TCP的统计信息
   > [root@xiesshavip002 ~]# netstat -su    # 显示所有UDP的统计信息
   > ```

4. 显示 PID 和进程名称

   > ```shell
   > [root@xiesshavip002 ~]# netstat -p
   > ```

5. 查看端口和服务

   > ```shell
   > [root@xiesshavip002 ~]# netstat -antp | grep ssh
   > [root@xiesshavip002 ~]# netstat -antp | grep 22
   > ```
   
6. 部分参数介绍

   > + -n： Local Address这列的host和port均用数字表示
   >
   > + -p：显示PID/Programe name 这列
   > + -a：列出全部端口
   > + -t：列出TCP端口
   > + -u：列出UDP端口
   > + -l：列出监听端口



# tar

1. 打包制定文件

   ```shell
   tar -cf archive.tar foo bar
   ```

2. 打包文件夹

   ```shell
   tar -cf Test.tar ./test/*
   ```

3. 打包+压缩文件夹

   ```shell
   tar -zcvf Tars_1.6.tar.gz ./Tars/*
   ```

4. 解压文件

   ```shell
   # 解压tar.gz
   tar -zxvf mysql-5.6.26.tar.gz
   ```

5. 参数

   > -v：显示处理的文件
   >
   > -x：解压
   >
   > -c：创建新文档，打包时用