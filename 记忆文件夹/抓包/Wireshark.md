# 第一章 过滤方法

1. 过滤源ip、目的ip

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

2. 端口过滤

   ```shell
   # 过滤源端口和目的端口为3000的数据包
   tcp.port == 3000
   
   # 过滤目的端口为3000
   tcp.dstport == 3000
   
   # 过滤源端口为3000
   tcp.srcport == 3000
   ```

3. 协议过滤

   ```shell
   # 在Filter框中输入协议名称，比如http
   ```

4. http模式过滤

   ```shell
   # 过滤GET请求
   http.request.method == "GET"
   
   # 过滤POST请求
   http.request.method == "POST"
   ```

5. and连接

   ```shell
   http.request.method == "POST" and ip.dst == 10.10.10.168
   ```

   



# 第二章 抓本地网络包

选中名称为<b style="color:red">Adapter for loopback traffic capture</b>的网卡