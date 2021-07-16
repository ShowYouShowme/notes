# 前提 root用户下执行

## git配置代理

1. 使用命令

   ```shell
   #http代理：
   git config --global http.proxy http://127.0.0.1:10800
   git config --global https.proxy https://127.0.0.1:10800
   ```
   
2. 编辑文件

   ```shell
   #在文件 ~/.gitconfig 添加：
   [http]
   proxy = http://127.0.0.1:10800
   [https]
   proxy = https://127.0.0.1:10800
   ```

3. 取消代理

   ```shell
   git config --global --unset http.proxy
   git config --global --unset https.proxy
   ```

## yum配置为阿里云源

## wget配置代理

修改配置文件`/etc/wgetrc`

```shell
# You can set the default proxies for Wget to use for http, https, and ftp.
# They will override the value in the environment.
https_proxy = http://proxy.yoyodyne.com:18023/
http_proxy = http://proxy.yoyodyne.com:18023/
ftp_proxy = http://proxy.yoyodyne.com:18023/

# If you do not want to use proxy at all, set this to off.
use_proxy = on
```

## centos全局代理配置



## 相关命令

```shell
source 把文件当成shell来执行
unset 删除环境变量
```



# 依赖环境

## 安装`glibc-devel`

```shell
yum install glibc-devel
```

## 安装`cmake-2.8.8`

```shell
# 安装g++ gcc
yum install gcc-c++ gcc

# 下载cmake
wget https://github.com/Kitware/CMake/archive/v2.8.8.tar.gz
tar -zxvf  v2.8.8.tar.gz
./bootstrap
make -j4
make install(如果make install失败，一般是权限不够，切换root进行安装)
```

## MySQL安装

1. 安装 ncurses、zlib

   ```shell
   yum install ncurses-devel
   yum install zlib-devel
   ```

2. 设置安装目录

   ```
   cd /usr/local
   mkdir mysql-5.6.26
   chown ${普通用户}:${普通用户} ./mysql-5.6.26 # root用户可以忽略
   ln -s /usr/local/mysql-5.6.26 /usr/local/mysql
   ```

3. 编译MySQL

   ```shell
   # MySQL源码下载到自己的Http服务器上
   cd /root
   wget https://dev.mysql.com/get/Downloads/MySQL-5.6/mysql-5.6.26.tar.gz
   tar -zxvf mysql-5.6.26.tar.gz
   cd ./mysql-5.6.26
   cmake . -DCMAKE_INSTALL_PREFIX=/usr/local/mysql-5.6.26 -DWITH_INNOBASE_STORAGE_ENGINE=1 -DMYSQL_USER=mysql -DDEFAULT_CHARSET=utf8 -DDEFAULT_COLLATION=utf8_general_ci
   make -j4
   make install
   ```

4. 配置MySQL

   ```shell
   yum install perl
   cd /usr/local/mysql
   useradd mysql
   rm -rf /usr/local/mysql/data
   mkdir -p /data/mysql-data
   ln -s /data/mysql-data /usr/local/mysql/data
   chown -R mysql:mysql /data/mysql-data /usr/local/mysql/data
   cp support-files/mysql.server /etc/init.d/mysql
   #如果/etc/目录下有my.cnf存在，需要把这个配置删除了
   rm -rf /etc/my.cnf
   yum install -y perl-Module-Install.noarch
   perl scripts/mysql_install_db --user=mysql
   vim /usr/local/mysql/my.cnf
   ```


# 开发环境

## web管理系统开发环境安装

1. 执行以下命令

   ```shell
   wget -O- https://raw.githubusercontent.com/creationix/nvm/v0.33.11/install.sh | bash
   source ~/.bashrc
   ```

2. node和pm2安装

   ```shell
   nvm install v8.11.3
   npm install -g pm2 --registry=https://registry.npm.taobao.org
   ```

   如果pm2无法识别

   ```shell
   npm i -g pm2
   ```

## c++ 开发环境安装

1. 下载Tars源码

   ```shell
   cd 
   git clone https://github.com/TarsCloud/Tars.git --recursive
   
   ```
   
2. 编译

   ```shell
   cd /root/Tars/
   git checkout v1.6.0
   cd /root/Tars/framework/build
   
   #### 这里应该用自己的build.sh 替换掉 原来的build.sh 或者修改原来的build.sh
   # 编译
   chmod u+x build.sh
   ./build.sh prepare
   # 修改./build.sh 用多核心编译 make -j4
   # 将框架编译成静态链接库
   ./build.sh all
   
   # 创建安装目录
   cd /usr/local
   mkdir tars
   chown ${普通用户}:${普通用户} ./tars/
   
   # 安装
   cd /root/Tars/framework/build
   ./build.sh install或者make install
   ```
   

编译要求MySQL的include路径<span style="color:violet">/usr/local/mysql/include</span>，lib的路径<span style="color:violet">/usr/local/mysql/lib/</span>



# 数据库环境初始化

## 添加用户

```mysql
# 主机名 修改成机器名字
mysql> grant all on *.* to 'tars'@'%' identified by 'tars2015' with grant option;
mysql> grant all on *.* to 'tars'@'localhost' identified by 'tars2015' with grant option;
mysql> grant all on *.* to 'tars'@'${主机名}' identified by 'tars2015' with grant option;

# 允许Root远程登录，可选
mysql> GRANT ALL PRIVILEGES ON *.* TO '${账号}'@'%' IDENTIFIED BY '${访问密码}' WITH GRANT OPTION;
mysql> flush privileges;
```

## 创建数据库

1. sql脚本在`TarsFramework/sql`目录下，修改部署ip的信息

   ```shell
   sed -i "s/192.168.2.131/${your machine ip}/g" `grep 192.168.2.131 -rl ./*`
   sed -i "s/db.tars.com/${your machine ip}/g" `grep db.tars.com -rl ./*`
   sed -i "s/10.120.129.226/${your machine ip}/g" `grep 10.120.129.226 -rl ./*`
   ```
   
2. 执行

   ```shell
   chmod u+x exec-sql.sh
   ./exec-sql.sh
   
   # 如果之前设置的数据库密码不是 root@appinside，则要修改sh文件
   ```

# Tars框架运行环境搭建

## 1 框架基础服务打包

+ 核心基础服务，必须手工部署

  > 1. tarsAdminRegistry
  >
  > 2. tarsregistry
  >
  > 3. tarsnode
  >
  > 4. tarsconfig
  >
  > 5. tarspatch

+ 普通基础服务

  > 1. tarsstat
  > 2. tarsproperty
  > 3. tarsnotify
  > 4. tarslog
  > 5. tarsquerystat
  > 6. tarsqueryproperty

+ 准备第一种服务

  ```shell
  cd /root/tars/TarsFramework/build
  make framework-tar
  ```

  会在当前目录生成framework.tgz 包

+ 第二种服务安装包可以单独准备

  ```shell
  make tarsstat-tar
  make tarsnotify-tar
  make tarsproperty-tar
  make tarslog-tar
  make tarsquerystat-tar
  make tarsqueryproperty-tar
  ```

  

## 2 安装框架核心基础服务

### 安装核心基础服务

1. 创建部署目录

   ```
   cd /usr/local
   mkdir app
   cd ./app
   mkdir tars
   ```

2. 将已打好的框架服务包复制到/usr/local/app/tars/，然后解压

   ```shell
   cp /root/Tars/framework/build/framework.tgz /usr/local/app/tars/
   cd /usr/local/app/tars
   tar xzfv framework.tgz
   ```

3. 修改配置文件

   ```shell
   cd /usr/local/app/tars
   sed -i "s/192.168.2.131/${your_machine_ip}/g" `grep 192.168.2.131 -rl ./*`
   sed -i "s/db.tars.com/${your_machine_ip}/g" `grep db.tars.com -rl ./*`
   sed -i "s/registry.tars.com/${your_machine_ip}/g" `grep registry.tars.com -rl ./*`
   sed -i "s/web.tars.com/${your_machine_ip}/g" `grep web.tars.com -rl ./*`
   ```

4. 启动tars框架服务

   ```shell
   chmod u+x tars_install.sh
   ./tars_install.sh
   ```

5. 部署管理平台并启动web管理平台

   ```
   tarspatch/util/init.sh
   ```

6. 注意 --TODO

   > 在管理平台上面配置tarspatch，注意需要配置服务的可执行目录(/usr/local/app/tars/tarspatch/bin/tarspatch)
   >
   > 在管理平台上面配置tarsconfig，注意需要配置服务的可执行目录(/usr/local/app/tars/tarsconfig/bin/tarsconfig)
   >
   > tarsnode需要配置监控，避免不小心挂了以后会启动，需要在crontab里面配置
   >
   > ```shell
   > * * * * * /usr/local/app/tars/tarsnode/util/monitor.sh
   > ```

### 服务扩容前安装tarsnode

单机部署服务测试时跳过，扩容时再执行！

## 3 安装web管理系统

1. 管理系统目录名称为web

2. 修改配置文件，将配置文件中的ip地址修改为本机ip地址

   ```shell
   cd /root/Tars/web
   sed -i 's/db.tars.com/${your_machine_ip}/g' config/webConf.js
   sed -i 's/registry.tars.com/${your_machine_ip}/g' config/tars.conf
   ```

3. 安装web管理页面依赖，启动web

   ```shell
   cd /root/Tars/web
   npm install --registry=https://registry.npm.taobao.org
   #先修改 package.json 里面的start项目 路径为bin/www
   npm run start
   ```

4. 创建日志目录

   ```shell
   mkdir -p /data/log/tars
   ```

5. 访问站点${your machine ip}:3000

   ```shell
   # 如果失败则需要关闭防火墙
   firewall-cmd --state # 查看防火墙状态
   systemctl stop firewalld.service # 停止防火墙
   systemctl disable firewalld.service  # 禁止防火墙开机启动
   ```

   

## 4 安装框架普通基础服务

1. tarsnotify部署发布
2. tarsstat部署发布
3. tarsproperty部署发布
4. tarslog部署发布
5. tarsquerystat部署发布，<span style="color:violet">选择非Tars协议，因为Web是以json协议来获取服务监控的数据的</span>
6. tarsqueryproperty部署发布，<span style="color:violet">选择非Tars协议，因为Web是以json协议来获取服务监控的数据的</span>



# 附录

## /etc/profile

> 常在里面修改环境变量，重启才能生效，对所有用户有效！`.bashrc`文件修改环境变量仅对当前用户有效
>
> ```shell
> PATH=$PATH:/usr/local/mysql/bin
> export PATH
> ```
>
> 常见系统环境变量：
>
> ```shell
> PATH:可执行文件查找目录
> HOME:当前用户主目录
> MAIL：是指当前用户的邮件存放目录。
> SHELL：是指当前用户用的是哪种Shell。
> HISTSIZE：是指保存历史命令记录的条数。
> LOGNAME：是指当前用户的登录名。
> HOSTNAME：是指主机的名称，许多应用程序如果要用到主机名的话，通常是从这个环境变量中来取得的。
> LANG/LANGUGE：是和语言相关的环境变量，使用多种语言的用户可以修改此环境变量。
> PS1：是基本提示符，对于root用户是#，对于普通用户是$。
> PS2：是附属提示符，默认是“>”。可以通过修改此环境变量来修改当前的命令符，比如下列命令会将提示符修改成字符串“Hello,My NewPrompt :) ”。
> ```
>
> 



# 遗留问题

1. tarsnode需要配置监控，避免不小心挂了以后会启动，需要在crontab里面配置/usr/local/app/tars/tarsnode/util/monitor.sh