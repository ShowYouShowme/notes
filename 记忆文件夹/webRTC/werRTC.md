# 一、 stun-turn服务搭建



## 1.1  turn

1. 安装依赖

   ```shell
   yum install -y openssl openssl-devel
   yum -y install libevent-devel
   ```

2. 安装服务

   ```shell
   git clone https://github.com/coturn/coturn
   cd coturn
   ./configure
   make
   make install
   ```

3. 配置

   ```shell
   cp examples/etc/turnserver.conf /usr/local/bin/turnserver.conf
   
   #修改配置文件
   #监听端口
   listening-port=3478
    
   #阿里云内网IP
   listening-ip=${IP}
    
   #阿里云外网IP地址
   external-ip=${IP}
   #访问的用户、密码
   user=yubao:000000
   ```

4. 启动服务

   ```shell
   cd /usr/local/bin
   turnserver -v -r 118.24.78.34:3478 -a -o
   ```



## 1.2 stun

1. 安装依赖

   ```shell
   yum install gcc gcc-c++
   yum install make
   yum install boost-devel # For Boost
   yum install openssl-devel # For OpenSSL
   ```

   

2. 安装stun服务

   ```shell
   wget http://www.stunprotocol.org/stunserver-1.2.7.tgz
   tar -zxvf stunserver-1.2.7.tgz
   cd stunserver
   make
   ```

3. 启动服务

   ```shell
   # 默认绑定UDP 端口,记得关闭防火墙
   ./stunserver --primaryport 3478 --verbosity 3
   ```

4. 测试

   ```shell
   ./stunclient 127.0.0.1 3478
   ```

   

