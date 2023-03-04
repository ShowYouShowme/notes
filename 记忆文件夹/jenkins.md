# 第一章 安装

Jenkins的功能是主动化构建（类似C++的build，比如打安卓包、ios包，java编译等），但是并没有自动化发布的功能。



**自动化发布的思路**

思路一

1. 利用命令scp将包上传到服务器 
2. 2.远程执行服务器的脚本来发布

思路二

1. 在服务器上部署一个express服务
2. 提供一个接口上传包
3. 提供一个接口发布项目
4. 利用postman来访问即可



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



# 第二章 添加节点

```shell
# 新节点安装jdk
yum install -y java-11-openjdk

# jenkins里配置新节点ip和账号密码

useradd jenkins
```

