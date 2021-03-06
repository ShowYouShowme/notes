### 课程目录介绍

+ Python介绍与安装
+ 变量、数字、序列、映射和集合
+ 条件与循环
+ 文件、输入输出、异常
+ 函数、模块
+ 面向对象编程
+ 多线程编程
+ 标准库
+ 第三方库
+ 综合项目
### 介绍和安装

+ 语言特点
	1. 语法简洁
	2. 跨平台
	3. 类库丰富
	4. 开放源码
	5. 可扩展，可以调用C/C++的库
+ 发展历史与版本
	+ 发展历史 
		1. 1990年诞生
		2. 2000年Python2.0发布
		3. 2008年Python3.0发布
		4. 2010年Python2.7发布(最后一个2.x版本)
	+ 版本
		1. Python2.x
		2. Python3.x
			1. 官方版本
			2. 发行版本[Anaconda](https://www.anaconda.com/)
	+ 开发工具
		1. [Python官方文档](https://docs.python.org)
		2. [iPython](https://ipython.org/)
		3. jupyter notebook，可以在网页编程
		4. sublime text 文本编辑器
		5. Pycharm 集成开发环境
		6. Pip 包管理器
+ 安装
	1. 安装python
	
	   1. Ubuntu18.04编译安装python3.7
	
	      ```shell
	      # 0 安装依赖
	      apt-get install zlib1g-dev libffi-dev gcc make
	      
	      # 1 下载安装包
	      wget https://www.python.org/ftp/python/3.7.1/Python-3.7.1.tgz
	      
	      # 2 解压
	      tar -zxvf Python-3.7.1.tgz
	      
	      # 3 编译安装
	      cd Python-3.7.1
	      ./configure
	      make
	      make install
	      
	      ```
	
	      
	
	2. 安装pycharm 
	
	3. 在终端里启动>python
	
	4. 在终端里退出>>>exit()
	
+ 源码编译安装

  1. 下载源码

     ```shell
     wget https://www.python.org/ftp/python/3.7.2/Python-3.7.2.tgz
     ```

  2. 安装依赖

     ```shell
     yum install -y gcc zlib* readline readline-devel libffi-devel openssl-devel
     ```

  3. 编译

     ```shell
     # 1 解压
     tar -zxvf Python-3.7.2.tgz
     
     # 2 进入目录
     cd ./Python-3.7.2
     
     # 3 配置 安装mod_wsgi会用到python的动态链接库
     ./configure --prefix=/usr/local/python3 --enable-shared
     
     # 4 编译
     make -j4
     
     # 5 安装
     make
     
     # 6 配置环境变量并注册动态链接库
     
     ## 6-1 配置环境变量
     vi /etc/profile
     export PATH=$PATH:/usr/local/python3/bin # 添加到文件末尾
     
     source /etc/profile
     
     ## 6-2 注册动态链接库
     vi /etc/ld.so.conf
     /usr/local/python3/lib # 添加到文件末尾
     ldconfig
     
     ```

     