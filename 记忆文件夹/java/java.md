# jre安装

+ 描述：jre是java Runtime Environment，java开发的程序运行依赖于它

+ 安装

  1. Ubuntu 18.04

     ```shell
     # step1
     apt-get install default-jre
     
     # step2 获取JAVA_HOME路径
     update-alternatives --config java 
     # 执行上述命令显示：/usr/lib/jvm/java-11-openjdk-amd64/bin/java
     # 显然JAVA_HOME 为/usr/lib/jvm/java-11-openjdk-amd64
     
     # step3 设置环境变量JAVA_HOME
     vim /etc/profile
     export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64/
     source /etc/profile
     ```

     

  



# jdk安装

+ 描述：jdk是Java Development Kit，包含了jre

+ 编译java需要用到；包含了开发和运行时的环境

  ```shell
  yum install java-1.8.0-openjdk* -y
  ```
  
+ 源码安装：推荐的方式

  ```ini
  ;下载压缩包
  tar -zxvf jdk-8u361-linux-x64.tar.gz
  mv jdk1.8.0_361/ ~/local/
  
  ;配置环境变量 .bashrc
  [enviroment]
  JAVA_HOME=$HOME/local/jdk1.8.0_361
  JRE_HOME=$JAVA_HOME/jre
  CLASS_PATH=.:$JAVA_HOME/lib/dt.jar:$JAVA_HOME/lib/tools.jar:$JRE_HOME/lib
  PATH=$PATH:$JAVA_HOME/bin:$JRE_HOME/bin
  export JAVA_HOME JRE_HOME CLASS_PATH PATH
  
  [测试]
  java -version
  ```

  






# maven安装

```shell
#下载安装包
wget https://mirrors.tuna.tsinghua.edu.cn/apache/maven/maven-3/3.6.3/binaries/apache-maven-3.6.3-bin.tar.gz --no-check-certificate

#解压
tar -zxvf apache-maven-3.6.3-bin.tar.gz

#移动到对应目录
mv apache-maven-3.6.3 ~/local/

#添加环境变量
vim ~/.bashrc

export PATH=/home/nash/local/apache-maven-3.6.3/bin:$PATH
```





# xxl-job

1. 下载

   ```shell
   wget https://github.com/xuxueli/xxl-job/archive/refs/tags/2.3.1.tar.gz
   ```

2. 安装maven 3.6

3. 编译xxl-job

   ```shell
   tar -zxvf 2.3.1.tar.gz
   cd xxl-job-2.3.1/xxl-job-admin/src/main/resources
   #修改数据库的用户名和密码
   vim application.properties
   
   #打包
   cd xxl-job-2.3.1/xxl-job-admin
   mvn package
   
   
   #打包执行器
   cd xxl-job-2.3.1/xxl-job-executor-samples/xxl-job-executor-sample-springboot
   mvn package
   
   #导入数据库
   mysql -uroot -ptars2015 < tables_xxl_job.sql
   
   
   #启动admin
   java -jar xxl-job-admin-2.3.1.jar
   
   #启动执行器
   java -jar xxl-job-executor-sample-springboot-2.3.1.jar
   
   #登录管理界面
   http://localhost:8080/xxl-job-admin 
   ```

4. 建议使用shell脚本

   ```ini
   [获取上个命令退出码]
   cmd = echo $?
   
   [执行node脚本]
   cmd = node path/to/your/script
   
   [node指定退出码]
   cmd = process.exit(123)
   ```

   
