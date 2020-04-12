# 1 Docker API

+ Registry API：存储docker镜像
+ Docker Hub API：与docker Hub集成的功能
+ Docker Remote API：与docker守护进程集成的API，本章重点介绍





# 2 访问docker API

1. 修改配置文件`/usr/lib/systemd/system/docker.service`

   ```shell
   变量ExecStart增加选项-H tcp://0.0.0.0:2375
   ```

2. 重新加载和启动docker守护进程

   ```shell
   systemctl --system daemon-reload
   ```

3. 访问

   ```shell
   docker -H 127.0.0.1:2375 info
   ```



# 3 测试 API



## 3.1 管理docker镜像

1. 获取镜像列表

   ```shell
   curl http://127.0.0.1:2375/images/json | python3 -m json.tool
   ```

2. 查看docker信息

   ```shell
   curl http://127.0.0.1:2375/info | python3 -m json.tool
   ```

3. 查询指定镜像的信息

   ```shell
   curl http://127.0.0.1:2375/images/f1cb7c7d58b7/json | python3 -m json.tool
   ```

4. 在Docker Hub上面查找镜像

   ```shell
   curl http://127.0.0.1:2375/images/search?term=nginx | python3 -m json.tool
   ```



## 3.2 管理docker容器

1. 列出正在运行的容器

   ```shell
   curl http://127.0.0.1:2375/containers/json | python3 -m json.tool
   ```

2. 列出全部容器

   ```shell
   curl http://127.0.0.1:2375/containers/json?all=1 | python3 -m json.tool
   ```

3. 创建容器

   ```shell
   curl -X POST -H 'Content-Type:application/json' http://127.0.0.1:2375/containers/create -d '{ "Image":"centos:7.6.1810" }'
   ```

   分行的格式

   ```shell
   curl -X POST -H "Content-Type:application/json" \
   http://127.0.0.1:2375/containers/create \
   -d \
   " \
   { \
   \"Image\":\"centos:7.6.1810\" \
   }"
   ```

4. 启动容器

   ```shell
   curl -X POST -H "Content-Type:application/json" http://127.0.0.1:2375/containers/8a4a1fc441ae/start -d {}
   ```

5. 获取指定容器信息

   ```shell
   curl http://127.0.0.1:2375/containers/8a4a1fc441ae/json | python3 -m json.tool
   ```



# 4 认证Docker Remote API



## 4.1 建立证书授权中心

1. 创建目录

   ```shell
   mkdir -p /home/docker
   cd /home/docker
   ```

2. 生成序列化记录文件

   ```shell
   echo 01 > ca.srl
   ```

3. 生成私钥

   ```shell
   openssl genrsa -des3 -out ca-key.pem
   
   # 密码暂时指定为:1234
   ```

4. 创建CA证书

   ```shell
   # 信息全部留空
   openssl req -new -x509 -days 365 -key ca-key.pem -out ca.pem
   ```

   

## 4.2 创建服务器证书和密钥

1. 创建服务器密钥

   ```shell
   openssl genrsa -des3 -out server-key.pem
   
   # 密码暂时指定为:5678
   ```

2. 创建服务器证书签名请求(CSR)

   ```shell
   openssl req -new -key server-key.pem -out server.csr
   
   # Common Name 设置为网站域名,其它选项留空
   ```

3. 对CSR签名

   ```shell
   openssl x509 -req -days 365 -in server.csr -CA ca.pem -CAkey ca-key.pem -out server-cert.pem
   ```

4. 清除服务器密钥的密码，否则docker守护进程启动时要输入密码

   ```shell
   openssl rsa -in server-key.pem -out server-key.pem
   ```

   

## 4.3 配置Docker守护进程

1. 复制证书和密钥到指定目录

   ```shell
   cp ./ca.pem server-cert.pem server-key.pem  /etc/docker/
   ```

2. 修改docker配置文件

   ```shell
             # vi /usr/lib/systemd/system/docker.service
             
             --tlsverify \
             --tlscacert=/etc/docker/ca.pem \
             --tlscert=/etc/docker/server-cert.pem \
             --tlskey=/etc/docker/server-key.pem \
   ```

3. 重新加载并启动Docker守护进程

   ```shell
   systemctl --system daemon-reload
   ```

   



## 4.4 创建客户端证书和密钥

1. 创建客户端密钥

   ```shell
   openssl genrsa -des3 -out client-key.pem
   ```

2. 创建客户端CSR

   ```shell
   openssl req -new -key client-key.pem -out client.csr
   ```

3. 添加客户端认证属性

   ```shell
   echo extendedKeyUsage = clientAuth > extfile.cnf
   ```

4. 对客户端CSR签名

   ```shell
   openssl x509 -req -days 365 -in client.csr -CA ca.pem -CAkey ca-key.pem -out client-cert.pem -extfile extfile.cnf
   ```

5. 清除客户端密钥的密码

   ```shell
   openssl rsa -in client-key.pem -out client-key.pem
   ```

   

## 4.5 开启客户端认证功能

1. 复制证书和密钥

   ```shell
   mkdir -p ~/.docker
   cp ca.pem ~/.docker/
   cp client-key.pem  ~/.docker/key.pem
   cp client-cert.pem ~/.docker/cert.pem
   chmod 0600 ~/.docker/key.pem ~/.docker/cert.pem
   ```

2. 测试TLS认证过的连接

   ```shell
   docker -H=docker.example.com:2376 --tlsverify info
   ```

   