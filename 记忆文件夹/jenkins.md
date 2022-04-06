# 第一章 安装



## 1.1 官方安装方式

```shell
wget -O /etc/yum.repos.d/jenkins.repo https://pkg.jenkins.io/redhat-stable/jenkins.repo --no-check-certificate

rpm --import https://pkg.jenkins.io/redhat-stable/jenkins.io.key
yum install fontconfig java-11-openjdk
yum install jenkins -y
systemctl start jenkins
systemctl enable jenkins
```



## 1.2 war包安装

```shell
yum install -y java-11-openjdk tomcat tomcat-webapps

# html 文件路径
cd /usr/share/tomcat/webapps/ROOT
rm -rf ./*
curl -O https://get.jenkins.io/war-stable/2.332.1/jenkins.war -L
jar -xvf jenkins.war
rm -f jenkins.war
systemctl start tomcat
systemctl enable tomcat
```

