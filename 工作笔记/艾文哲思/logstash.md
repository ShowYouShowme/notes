# 安装

+ 安装步骤

  ```shell
  # 安装jdk
  yum install -y java-1.8.0-openjdk-devel.x86_64
  
  wget https://artifacts.elastic.co/downloads/logstash/logstash-6.5.2.tar.gz
  
  tar -zxvf logstash-6.5.2.tar.gz
  
  mv logstash-6.5.2 logstash
  
  # 修改配置文件 logstash/config
  
  cd logstash/config
  
  cp logstash-sample.conf logstash.conf
  
  # 修改配置文件,参考下面
  
  # 启动logstash
  ../bin/logstash -f logstash.conf
  ```

+ `logstash.conf`配置内容

  ```shell
  input {
          file{
                  type => "syslog"
                  path => ["/var/log/t1.log", "/var/log/t2.log"]
  }
  }
  
  output {
          stdout {
                  codec => rubydebug
  }
  }
  ```

+ java环境变量配置[此处可忽略]

  ```shell
  JAVA_PATH=/usr/java/jdk1.8.0_231/bin:/usr/java/jdk1.8.0_231/jre/bin
  JAVA_HOME=/usr/java/jdk1.8.0_231
  export PATH=$PATH:/usr/java/jdk1.8.0_231/bin:/usr/java/jdk1.8.0_231/jre/bin
  ```

  