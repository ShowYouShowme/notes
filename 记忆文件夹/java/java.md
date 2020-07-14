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
+ 安装