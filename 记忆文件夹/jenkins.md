# 第一章 安装

Jenkins的功能是自动化构建（类似C++的build，比如打安卓包、ios包，java编译等），但是并没有自动化发布的功能。



**自动化发布的思路**

思路一

1. 利用命令scp将包上传到服务器 
2. 2.远程执行服务器的脚本来发布



思路二

1. 在服务器上部署一个express服务
2. 提供一个接口上传包
3. 提供一个接口发布项目
4. 利用postman来访问即可



思路三

1. 在生产、测试、开发服务器上分别源码部署一套jenkins
2. gitea部署在云上
3. 用特定用户启动jenkins，然后执行自动化构建、发布的流程



## 1.1 官方安装方式[推荐]

1. 删除旧版的jdk

   ```shell
   查看
   rpm -qa | grep java
   rpm -qa | grep jdk
   批量卸载
   rpm -qa | grep jdk | xargs rpm -e --nodeps
   rpm -qa | grep java | xargs rpm -e --nodeps
   
   ```

2. 安装jenkins

   ```shell
   wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo --no-check-certificate
   
   rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
   yum install fontconfig java-11-openjdk jenkins -y
   yum install -y java-11-openjdk java-11-openjdk-devel
   systemctl start jenkins
   systemctl enable jenkins
   ```

   



## 1.2 war包安装

```shell
yum install -y java-11-openjdk java-11-openjdk-devel tomcat tomcat-webapps

# html 文件路径
cd /usr/share/tomcat/webapps/ROOT
rm -rf ./*
curl -O https://get.jenkins.io/war-stable/2.332.1/jenkins.war -L
jar -xvf jenkins.war
rm -f jenkins.war
systemctl start tomcat
systemctl enable tomcat
```



## 1.3 源码安装

源码安装启动用户是执行命令的用户，可以方便操作文件和目录。用来部署服务非常简单！

1. 安装java

   ```shell
   wget https://builds.openlogic.com/downloadJDK/openlogic-openjdk/8u362-b09/openlogic-openjdk-8u362-b09-linux-x64.tar.gz --no-check-certificate
   
   tar -zxvf openlogic-openjdk-8u362-b09-linux-x64.tar.gz
   mv openlogic-openjdk-8u362-b09-linux-x64 ~/local/openjdk8
   
   # 配置环境变量
   vim ~/.bashrc
   
   export JAVA_HOME=$HOME/local/openjdk8
   export JRE_HOME=$JAVA_HOME/jre
   export PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
   export CLASSPATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
   ```

2. 安装tomcat

   ```shell
   wget https://dlcdn.apache.org/tomcat/tomcat-9/v9.0.73/bin/apache-tomcat-9.0.73.tar.gz --no-check-certificate
   
   tar -zxvf apache-tomcat-9.0.73.tar.gz
   mv apache-tomcat-9.0.73.tar.gz ~/tomcat-9.0.73
   ```

3. 安装jenkins

   ```shell
   wget https://get.jenkins.io/war-stable/2.346.1/jenkins.war --no-check-certificate
   
   # 缺少会报错
   yum -y install fontconfig
   
   mv jenkins.war $HOME/local/tomcat-9.0.73/webapps
   ```

4. 启动tomcat

   ```shell
   # 启动命令
   $HOME/local/tomcat-9.0.73/bin/startup.sh
   
   # 查看端口是否监听
   netstat -lnt | grep 8080
   
   # 关闭命令
   $HOME/local/tomcat-9.0.73/bin/shutdown.sh
   ```

5. 访问jenkins

   ```ini
   [浏览器访问]
   url = http://120.25.248.58:8080/jenkins/
   
   [命令行访问]
   cmd = curl http://120.25.248.58:8080/jenkins/
   ```

6. 另一种启动方式

   ```shell
   # [推荐]不需要tomcat，此时访问url就是 http://120.25.248.58:8080/ 
   java -jar jenkins.war
   
   
   # jenkins.service
   
   [Unit]
   Description=jenkins daemon
   After=network.target
   
   [Service]
   Group = terry
   User  = terry
   Type=simple
   ExecStart=/home/terry/local/openjdk8/bin/java -jar /home/terry/doc/jenkins.war
   WorkingDirectory=/home/terry/log
   
   [Install]
   WantedBy=multi-user.target
   ```
   
   



# 第二章 添加节点

```shell
# 新节点安装jdk
yum install -y java-11-openjdk

# jenkins里配置新节点ip和账号密码

useradd jenkins
```







# 第三章 配置git

第一次进入管理后台时，安装推荐的全部插件即可。

1. 源码安装git

2. 全局工具里面配置git的路径

   ```shell
   主页面 > 系统管理 > 全局工具配置 > Path to Git executable
   
   填入 = /home/terry/local/git/bin/git
   ```






# 第四章 构建配置

1. General：大部分项目不需要配置，最多只需要配置参数化构建

   + 选项

     ```ini
     [GitHub 项目]
     ; 如果项目是github项目,可以填入url
     
     [Throttle builds]
     ; 限制构建速度
     
     [丢弃旧版的构建]
     
     [参数化构建过程]
     
     [在必要的时候并发构建]
     ```

   + 常用选项：参数化构建

     ```shell
     # 必须先安装插件 Git Parameter
     1. 勾选参数化构建过程
     2. 选择Git参数
     3. 名称 = tag
     4. 描述 = 选择线上tag
     5. 参数类型 = 标签
     6. 默认值 = v1.0.0
     ```

2. 源码管理：配置git的仓库地址和证书

   ```shell
   Branches to build
   	# 上面的参数化过程的名称
   	指定分支 = ${tag}
   ```

   

3. 构建触发器

   ```ini
   定时构建 = 不管SVN或Git中数据有无变化，均执行定时化的构建任务
   ; 每天12点构建
   example1 = 0 12 * * *
   ; 每天00:00 构建
   example2 =0 0 * * *
   
   轮询SCM = 只要SVN或Git中数据有更新，则执行构建任务；
   ```

   

4. 构建环境：Add timestamps to the Console Output

5. 构建：执行shell

   ```shell
   # 执行$HOME/.bashrc 更新PATH
   # $JOB_NAME 是任务名，比如game
   source $HOME/.bashrc
   echo "job name = $JOB_NAME"
   ls -l
   npm install
   tsc
   rm -rf $HOME/app/$JOB_NAME
   cd ..
   mv $JOB_NAME $HOME/app/
   cd $HOME/app/$JOB_NAME
   echo $PWD
   pm2 delete jenkins_demo
   pm2 start bin/index.js --name jenkins_demo
   ```




# 第五章 使用Root启动服务

构建完成后，需要把可执行文件copy到指定目录，并且重启服务，这时往往需要root权限

1. 修改服务文件

   ```shell
   vim /lib/systemd/system/jenkins.service
   
   User=root
   Group=root
   ```

2. 修改jenkins home相关文件夹权限

   ```shell
   chown -R root:root /var/lib/jenkins
   chown -R root:root /var/cache/jenkins
   chown -R root:root /var/log/jenkins
   ```

3. 重启服务

   ```shell
   systemctl daemon-reload
   systemctl restart jenkins
   ```






# 第六章 常用插件

```ini
[中文语言包]
name = Locale plugin

[Git参数化构建]
name = Git Parameter

[SSH远程发布]
name = Publish Over SSH

[用户权限管理]
; 安装后需要进入  全局安全配置 --修改授权策略 为 Role-Based Strategy
name = Role-based Authorization

; 权限配置，先设置用户角色，然后再授予具体的权限
; Manager Roles 里面Global roles 下，填入Role 名称并点击Add
; 权限勾选 全部-Read 任务-[Build、Cancel、Read]即可
; Assign Roles 里面Global roles 下， 勾选特定用户为Authenticated Users
```



# 第七章 构建脚本示范

1. 不使用插件git，cd到指定目录执行命令[推荐的做法]

   + 执行具体命令

     ```shell
     source /etc/profile
     cd /data/wwwroot/rummy-web
     git pull
     npm run build
     ```

   + 执行make

     ```shell
     source /etc/profile
     cd /data/rm/gateway
     make
     ```
     
   + 远程构建

     ```shell
     ssh stage 'source /etc/profile && \
               cd /data/rummy-game/cron && \
               make'
     ```

2. 使用git插件，构建后cp -f src dest 配置 pm2的watch[不推荐的做法，除非是用docker、k8s]

   ```shell
   source /etc/profile
   git submodule init
   git submodule update --recursive --remote
   protoc --go_out=. --go-grpc_out=. common/netmsg.proto
   protoc --go_out=. --go-grpc_out=. common/apimsg.proto
   protoc --go_out=. --go-grpc_out=. common/errcode.proto
   go mod tidy
   go build
   cp -f gateway /data/rm/gateway/
   # 重启服务
   pm2 stop gateway && pm2 start gateway
   ```

   
