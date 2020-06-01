## 1 TCP的特点

***



### 1 编号系统

***

+ 字节号

  ```shell
  0~(2^32 - 1)之间的一个随机数作为第一个字节的编号
  ```

+ 序号

  ```shell
  每个报文段的序号就是该报文段中第一个数据字节的序号
  ```

+ 确认号

  ```shell
  期望收到的下一个字节的编号
  ```

### 2 流量控制

***

+ 接收方要对发送tcp能够发送多少数据进行控制
+ 发送方要对能够接受多少用户进程传来的数据进行控制

### 3 差错控制

***

+ 报文可能会出错
+ 报文可能会丢失
+ 报文可能会受损

### 4 拥塞控制

***

+ tcp要考虑到网络的拥塞程度





## 报文段

***



### 1 格式

***

1. 格式定义

   ```c
   class TCPHeader
   {
       unsigned short  src_port;   // 源端口
       unsigned short  dst_port;   // 目的端口
       unsigned int    seq_num;    // 序号
       unsigned int    ack_num;    // 确认号
       unsigned int:4  hlen;       // 首部长度，指示tcpheader的大小
                int:6  reserved;   // 保留
                int:1  urg;        // 紧急指针有效
                int:1  ack;        // 确认是有效的
                int:1  psh;        // 请求推送
                int:1  rst;        // 连接复位
                int:1  syn;        // 同步序号
                int:1  fin;        // 终止连接
       unsigned short  rwnd;       // 窗口尺寸
       unsigned short  check_sum;  // 校验和
       unsigned short  urgent_pointer; // 紧急指针
       unsigned char[40] options;      // 选项和填充
   };
   ```

   

### 2 封装

***

```shell
# 1-- 应用层数据

# 2-- tcp首部 + 应用层数据

# 3-- ip首部 + tcp首部 + 应用层数据

# 4-- 帧首部 + ip首部 + tcp首部 + 应用层数据
```





## 2 tcp连接

***



### 1 连接建立

***

+ 三向握手

  ```shell
  # 第一次握手
  seq_num = 8000
  syn = 1
  
  # 第二次握手
  seq_num = 15000
  ack_num = 8001
  syn		  = 1
  ack			= 1
  rwnd	  = 5000
  
  # 第三次握手
  seq_num = 8000
  ack_num = 150001
  ack			= 1
  rwnd		= 10000
  ```

  

+ 同时打开 ==> 两个tcp都向对方发送SYN + ACK报文段

+ SYN洪泛攻击

### 2 数据传送

***



### 3 连接终止

***



### 4 连接复位

***



## 3 状态转换图

***

