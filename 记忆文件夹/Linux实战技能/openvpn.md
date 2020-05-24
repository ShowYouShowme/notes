# 安装openvpn

***



## 1-安装openvpn

***

```shell
yum install openvpn -y
```



## 2-创建 服务器证书密钥

```shell
# 在/root 执行
wget https://github.com/OpenVPN/easy-rsa/archive/v3.0.5.zip
yum install -y unzip
unzip v3.0.5.zip
mv easy-rsa-3.0.5 easy-rsa

cp -a easy-rsa/ /etc/openvpn/
cd /etc/openvpn/easy-rsa/easyrsa3
cp vars.example vars
vim vars

## 以下为vars文件的内容
set_var EASYRSA_REQ_COUNTRY     "CN"
set_var EASYRSA_REQ_PROVINCE    "Henan"
set_var EASYRSA_REQ_CITY        "Zhengzhou"
set_var EASYRSA_REQ_ORG         "along"
set_var EASYRSA_REQ_EMAIL       "along@163.com"
set_var EASYRSA_REQ_OU          "My OpenVPN"
############################################

# 1--初始化
 ./easyrsa init-pki

# 2--创建根证书
 ./easyrsa build-ca # 输入密码和域名,这里域名是along
 
# 3--创建服务端证书
./easyrsa gen-req server nopass #Common name 为along521

# 4--签约服务端证书
./easyrsa sign server server # 1-- 输入'yes' 2-- 输入之前的密码

# 5--创建Diffie-Hellman，确保key穿越不安全网络的命令
./easyrsa gen-dh
```



## 3-创建客户端证书

```shell
cd /root
mkdir client
cp -r /etc/openvpn/easy-rsa client/
cd client/easy-rsa/easyrsa3/

# 1--初始化
./easyrsa init-pki # 输入yes确定

# 2--创建客户端key以及生成证书
 ./easyrsa gen-req along # 1--输入密码  2--Common Name 是 along
 
# 3--签约证书
cd /etc/openvpn/easy-rsa/easyrsa3/
./easyrsa import-req /root/client/easy-rsa/easyrsa3/pki/reqs/along.req along 
./easyrsa sign client along # 1-- 输入'yes' 2--输入密码
 
```



## 4- 复制文件

***

1. 复制服务器文件

   ```shell
   cp /etc/openvpn/easy-rsa/easyrsa3/pki/ca.crt /etc/openvpn/
   cp /etc/openvpn/easy-rsa/easyrsa3/pki/private/server.key /etc/openvpn/
   cp /etc/openvpn/easy-rsa/easyrsa3/pki/issued/server.crt /etc/openvpn/
   cp /etc/openvpn/easy-rsa/easyrsa3/pki/dh.pem /etc/openvpn/
   ```

   

2. 复制客户端文件

   ```shell
   cp /etc/openvpn/easy-rsa/easyrsa3/pki/ca.crt /root/client/
   cp /etc/openvpn/easy-rsa/easyrsa3/pki/issued/along.crt /root/client/
   cp /root/client/easy-rsa/easyrsa3/pki/private/along.key /root/client
   ```



## 5-编辑配置文件

***

1. 查找模板配置文件路径

   ```shell
   rpm -ql openvpn |grep server.conf
   
   # 以下是输出
   /usr/share/doc/openvpn-2.4.9/sample/sample-config-files/roadwarrior-server.conf
   /usr/share/doc/openvpn-2.4.9/sample/sample-config-files/server.conf
   /usr/share/doc/openvpn-2.4.9/sample/sample-config-files/xinetd-server-config
   ```

2. 复制配置文件到相应路径

   ```shell
   cp /usr/share/doc/openvpn-2.4.9/sample/sample-config-files/server.conf  /etc/openvpn
   ```

3. 编辑配置文件

   ```shell
   vim  /etc/openvpn/server.conf
   
   # 以下为内容
   local 0.0.0.0     #监听地址
   port 11194     #监听端口
   proto tcp     #监听协议
   dev tun     #采用路由隧道模式
   ca /etc/openvpn/ca.crt      #ca证书路径
   cert /etc/openvpn/server.crt       #服务器证书
   key /etc/openvpn/server.key  # This file should be kept secret 服务器秘钥
   dh /etc/openvpn/dh.pem     #密钥交换协议文件
   server 10.8.0.0 255.255.255.0     #给客户端分配地址池，注意：不能和VPN服务器内网网段有相同
   ifconfig-pool-persist ipp.txt
   push "redirect-gateway def1 bypass-dhcp"      #给网关
   push "dhcp-option DNS 8.8.8.8"        #dhcp分配dns
   client-to-client       #客户端之间互相通信
   keepalive 10 120       #存活时间，10秒ping一次,120 如未收到响应则视为断线
   comp-lzo      #传输数据压缩
   max-clients 100     #最多允许 100 客户端连接
   user openvpn       #用户
   group openvpn      #用户组
   persist-key
   persist-tun
   status /var/log/openvpn/openvpn-status.log
   log         /var/log/openvpn/openvpn.log
   verb 3
   ```



## 6-额外配置

***

```shell
# 配置日志文件夹
mkdir /var/log/openvpn
chown -R openvpn.openvpn /var/log/openvpn/

# 配置文件夹权限
chown -R openvpn.openvpn /etc/openvpn/*

# 路由配置 IP是客户端分配地址池
 iptables -t nat -A POSTROUTING -s 10.8.0.0/24 -j MASQUERADE
 iptables -vnL -t nat
 
 # 打开路由转发
 vim /etc/sysctl.conf
 
 # 增加下面一行
 net.ipv4.ip_forward = 1
 
 sysctl -p
```



## 7-启动openvpn服务

***

```shell
openvpn --daemon --config /etc/openvpn/server.conf
```







# 客户端配置

***

1. 下载客户端

   ```shell
   # 地址一
   https://openvpn.net/client-connect-vpn-for-windows/
   
   # 地址二
   百度云盘
   ```

   

2. 编辑配置文件`client.ovpn`

   ```shell
   client
   dev tun
   proto tcp    
   remote 47.112.251.164 11194
   resolv-retry infinite
   nobind
   persist-key
   persist-tun
   ca ca.crt
   cert along.crt    
   key along.key      
   comp-lzo
   verb 3
   ```

3. 把服务器里面的client文件夹的证书相关文件下载到本地

   ```shell
   along.crt
   along.key
   ca.crt
   ```

4. 连接

5. 测试是否成功

   ```shell
   # ifconfig 服务器网卡tun0的ip
   ping 10.8.0.1
   ```

   

   