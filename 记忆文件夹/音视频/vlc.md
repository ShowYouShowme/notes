# 一、sdp文件编写

用VLC接受RTP流时，播放器需要根据SDP文件描述的信息知道如何播放输入源



## 1.1 H264流

```shell
v=0
m=video 1234 RTP/AVP 96
a=rtpmap:96 H264/90000
c=IN IP4 127.0.0.1
```



## 1.2 PS流

```SHELL
s=MPEG Program Stream, streamed by XXXX  
m=video 1234 RTP/AVP 96  
a=rtpmap:96 MP2P/90000
c=IN IP4 127.0.0.1
```



## 1.3 TS流

```SHELL
s=MPEG Transport Stream, streamed by XXXX  
m=video 1234 RTP/AVP 96  
a=rtpmap:96 MP2T/90000
c=IN IP4 127.0.0.1
```





s=参数：对流名称的说明，可以省略

m=参数后跟的信息：video <接收端口号>  RTP/AVP  <RTP负载类型>

a=参数跟的信息：rtpmap: <RTP负载类型> <数据的封装格式>/<时间戳的时钟频率>

c=参数跟的信息：IN  IP4 <接收端IP地址>

