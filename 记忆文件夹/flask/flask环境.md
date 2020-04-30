## 环境要求

***

1. Python3.3或更高的版本

2. 安装virtualenv

   ```shell
   pip3 install virtualenv
   ```

3. 创建虚拟环境

   ```shell
   mkdir newproj
   cd newproj
   
   # 使用默认的python解释器创建虚拟环境
   virtualenv venv
   
   # 使用指定的python解释器创建虚拟环境[推荐的方式]
   virtualenv -p /usr/bin/python3.7 venv
   ```

4. 进入虚拟环境

   ```shell
   source venv/bin/activate
   ```

5. 安装flask[在虚拟环境中运行]

   ```shell
   # 在虚拟环境里运行
   pip3 install Flask
   ```

6. 执行python脚本

   ```shell
   # 在虚拟环境里执行
   ```

   



## virtualenv相关命令

***

1.  退出虚拟环境

   ```shell
   # 在虚拟环境中运行
   deactivate
   ```

2. 查看虚拟环境详细信息

   ```shell
   # 可以看到虚拟环境使用的python版本
   virtualenv -v
   ```



## pip 与pip3

***

+ 使用pip3命令安装的库在`python3.x/site-packages`
+ 使用pip命令安装的库在`python2.x/site-packages`

