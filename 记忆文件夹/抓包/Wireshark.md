# 第一章 过滤方法

1. 抓取某个服务器端口的数据包

   ```shell
   (ip.src == 18.163.100.26 and tcp.srcport == 443) or (ip.dst == 18.163.100.26 and tcp.dstport == 443)
   
   #然后 右键一个包,追踪流 --- TCP流
   
   #c-s模式下, 可以用CLIENT_IP:CLIENT_PORT 区分一个连接
   #1--先用tcp.port==server_port 找到全部链接到server的链接
   #2--用客户端连接server
   #3--根据客户端的ip和port来跟踪流即可
   
   
   #设置时间显示格式：
   #视图--时间显示格式--时间
   ```

   

2. 过滤源ip、目的ip

   ```shell
   # 过滤目的ip
   ip.dst==10.10.10.168
   
   # 过滤源ip
   ip.src==10.10.10.168
   
   # 不等于
   ip.src != 10.10.10.177
   
   # ip地址为10.10.10.168
   ip.addr == 10.10.10.168
   ```

3. 端口过滤

   ```shell
   # 过滤源端口和目的端口为3000的数据包
   tcp.port == 3000
   
   # 过滤目的端口为3000
   tcp.dstport == 3000
   
   # 过滤源端口为3000
   tcp.srcport == 3000
   ```

4. 协议过滤

   ```shell
   # 在Filter框中输入协议名称，比如http
   ```

5. http模式过滤

   ```shell
   # 过滤GET请求
   http.request.method == "GET"
   
   # 过滤POST请求
   http.request.method == "POST"
   
   # 过滤指定域名
    http.host == www.feifeishijie.com
   ```

6. and连接

   ```shell
   http.request.method == "POST" and ip.dst == 10.10.10.168
   ```

   



# 第二章 抓本地网络包

选中名称为<b style="color:red">Adapter for loopback traffic capture</b>的网卡