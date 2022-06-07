# 第一章 负载均衡



## 1.1 负载均衡策略

| 策略             | 说明            |
| ---------------- | --------------- |
| 轮询             | 默认方式        |
| weight           | 权重方式        |
| ip_hash          | 根据ip分配方式  |
| least_conn       | 最少连接方式    |
| fair(第三方)     | 响应时间方式    |
| url_hash(第三方) | 根据URL分配方式 |



## 1.2 TCP负载均衡

```nginx
# 默认使用轮询的策略
# 如果server只有一个，就变成了TCP反向代理
stream {
  upstream test_mysql {
    server 192.168.0.68:8080;
    server 192.168.0.72:80;
  }
  server {
    listen 10086 so_keepalive=on;				# 开启 TCP 存活探测
    proxy_connect_timeout 10s;					# 连接超时时间
    proxy_timeout 300s;							# 端口保持时间
    proxy_pass test_mysql;
  }
}

```



## 1.3 haproxy TCP负载均衡

1. 安装

   ```shell
   # ubuntu 20.04
   sudo apt install software-properties-common
   sudo add-apt-repository ppa:vbernat/haproxy-2.5
   sudo apt update
   sudo apt install haproxy
   ```

2. 配置

   ```shell
   # 管理后台：http://192.168.0.66:8888/haproxy?stats
   # 配置文件haproxy.cfg 最后加上
   # 如果server 只配置一个就是TCP反向代理了
   frontend http_front
      bind *:8888
      stats uri /haproxy?stats
      default_backend http_back
   
   backend http_back
      balance roundrobin
      server web_server_1 192.168.0.68:8080 check
      server web_server_2 192.168.0.72:80 check
   ```




## 1.4 lvs 负载均衡

配置复杂，推荐使用nginx或者haproxy。

### 模式

1. LVS-DR：直接路由。Director和RealServer都在同一个局域网内
2. LVS-TUN：隧道模式
3. LVS-NAT：地址转换。 使用NAT模式将需要两个不同网段的IP，一个IP接受外部请求服务，一般为外网ip，此IP称为VIP，一个IP与后realserver同一地址段，负责相互通信，称为DIP。后端realserver的网关地址需指向DIP。同时需开启linux内核的数据包转发功能



### 调度算法

1. 轮叫调度 rr

2. 加权轮叫 wrr

3. 最少链接 lc

4. 加权最少链接 wlc

5. 基于局部性的最少连接调度算法 lblc

6. 复杂的基于局部性最少的连接算法 lblcr

7. 目标地址散列调度算法 dh

8. 源地址散列调度算法 sh



### DR模式配置

1. 机器ip

   > 三台server的ip
   >
   > direct_server:192.168.0.66
   >
   > real_server1:192.168.0.68
   >
   > real_server2:192.168.0.72
   >
   > vip:192.168.0.166 （Virtual ip）

2. 配置direct_server

   ```shell
   #! /bin/bash
   echo 1 > /proc/sys/net/ipv4/ip_forward
   ipv=/sbin/ipvsadm
   vip=192.168.0.166 # 虚拟IP
   rs1=192.168.0.68
   rs2=192.168.0.72
   ifconfig ens32:0 $vip broadcast $vip netmask 255.255.255.255 up
   route add -host $vip dev ens32:0
   
   ipvsadm -C
   ipvsadm -A -t $vip:8080 -s rr 
   ipvsadm -a -t $vip:8080 -r $rs1:8080 -g
   ipvsadm -a -t $vip:8080 -r $rs2:8080 -g
   ```

3. 配置real_server

   ```shell
   #! /bin/bash
   vip=192.168.0.166
   ifconfig lo:0 $vip broadcast $vip netmask 255.255.255.255 up
   route add -host $vip lo:0
   echo "1" >/proc/sys/net/ipv4/conf/lo/arp_ignore
   echo "2" >/proc/sys/net/ipv4/conf/lo/arp_announce
   echo "1" >/proc/sys/net/ipv4/conf/all/arp_ignore
   echo "2" >/proc/sys/net/ipv4/conf/all/arp_announce
   ```

4. 查看虚拟ip

   ```shell
   ifconfig
