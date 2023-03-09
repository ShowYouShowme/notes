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

```shell
wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo --no-check-certificate

rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
yum install fontconfig java-11-openjdk jenkins -y
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

   



# 第二章 添加节点

```shell
# 新节点安装jdk
yum install -y java-11-openjdk

# jenkins里配置新节点ip和账号密码

useradd jenkins
```



