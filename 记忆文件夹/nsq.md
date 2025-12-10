# 第一章 安装

```shell
wget https://s3.amazonaws.com/bitly-downloads/nsq/nsq-1.3.0.linux-amd64.go1.21.5.tar.gz
tar -zxvf nsq-1.3.0.linux-amd64.go1.21.5.tar.gz 
```



# 第二章 组件介绍



## 2.1 **nsqd**

- **作用**：消息的核心存储和转发；**单节点时可以只部署nsqd**
- **特点**：
  - 真正持有消息的节点
  - 每个 `nsqd` 是一个独立的队列实例
  - 接收生产者消息、写入磁盘（持久化）、发送给消费者
  - 可水平扩展，通过多个 `nsqd` 组成集群
- **端口**：
  - TCP 端口：消费者连接、生产者连接
  - HTTP 端口：监控、统计、调试接口



## 2.2 **nsqlookupd**

- **作用**：注册和发现 `nsqd` 节点
- **特点**：
  - 每个 `nsqd` 启动时会向 `nsqlookupd` 注册自己
  - 消费者可以向 `nsqlookupd` 查询哪些 `nsqd` 提供了特定 topic
  - 去中心化设计，可以部署多个 `nsqlookupd` 实现高可用
- **注意**：
  - `nsqlookupd` 本身不存储消息
  - 类似于“服务注册中心”



## 2.3 nsqadmin  

+ 管理后台



##  2.4 **topic / channel**

- **topic**：消息主题
  - 生产者发送消息到 topic
  - 一个 topic 对应一类消息
- **channel**：消息通道
  - 消费者订阅 channel
  - 同一 channel 的每条消息只会被一个消费者消费（队列模式）
  - 同一 topic 可以有多个 channel ，发送到topic的消息会被复制到每一个channel



## 2.5 端口介绍



### 2.5.1 nsqd

| 端口      | 作用                       | 默认值   |
| --------- | -------------------------- | -------- |
| TCP 端口  | 消费者订阅、生产者发送消息 | **4150** |
| HTTP 端口 | 监控、调试接口、消息查询   | **4151** |



### 2.5.2 nsqlookupd

| 端口      | 作用                              | 默认值   |
| --------- | --------------------------------- | -------- |
| TCP 端口  | nsqd 节点注册                     | **4160** |
| HTTP 端口 | 消费者 / 生产者查询 nsqd 节点信息 | **4161** |



### 2.5.3 nsqadmin

| 端口      | 作用         | 默认值   |
| --------- | ------------ | -------- |
| HTTP 端口 | Web 管理界面 | **4171** |



## 2.6 启动命令



### 2.6.1 启动nsqlookupd

```ini
nsqlookupd
```



### 2.6.2 启动nsqd

```ini
; 选项lookupd-tcp-address指定nsqlookupd的地址
; broadcast-address 向nsqlookupd注册自己的ip地址
nsqd --lookupd-tcp-address=127.0.0.1:4160 --broadcast-address=10.100.5.107
```



### 2.6.3 启动nsqadmin

```ini
; 选项lookupd-http-address指定nsqlookupd的HTTP接口地址
nsqadmin --lookupd-http-address=127.0.0.1:4161 
```



## 2.7 nsqd常用配置项



### 2.7.1 网络相关

| 配置项                     | 默认值          | 说明                                             |
| -------------------------- | --------------- | ------------------------------------------------ |
| `--tcp-address`            | `0.0.0.0:4150`  | TCP 服务监听地址（生产者/消费者连接）            |
| `--http-address`           | `0.0.0.0:4151`  | HTTP 服务监听地址（管理、stats、调试）           |
| `--broadcast-address`      | 系统自动获取    | 当 nsqd 在集群内被发现时向 nsqlookupd 广播的地址 |
| `--tls-cert` / `--tls-key` | -               | 启用 TLS 加密                                    |
| `--max-body-size`          | `1048576` (1MB) | 单条消息最大字节数                               |



### 2.7.2 消息存储/内存

| 配置项              | 默认值    | 说明                                          |
| ------------------- | --------- | --------------------------------------------- |
| `--data-path`       | `./data`  | 消息持久化路径                                |
| `--mem-queue-size`  | `10000`   | 内存队列大小（消息数）                        |
| `--max-msg-size`    | `1048576` | 单条消息最大大小                              |
| `--max-msg-timeout` | `1h`      | 消息超时最大值                                |
| `--msg-timeout`     | `60s`     | 默认消息超时时间（消费者 ack 超过时间后重发） |



### 2.7.3 日志 / 调试

| 配置项             | 默认值 | 说明                              |
| ------------------ | ------ | --------------------------------- |
| `--verbose`        | false  | 是否打印调试日志                  |
| `--logger-level`   | info   | 日志级别（debug/info/warn/error） |
| `--logger-logfile` | -      | 日志文件路径                      |
| `--statsd-address` | -      | 用于接入 StatsD 监控              |



### 2.7.4 nsqlookupd / 集群相关

| 配置项                  | 默认值 | 说明                                                         |
| ----------------------- | ------ | ------------------------------------------------------------ |
| `--lookupd-tcp-address` | -      | nsqd 启动时注册到的 nsqlookupd TCP 地址（可以多个，用逗号分隔） |
| `--broadcast-address`   | 自动   | 向 nsqlookupd 广播自己可访问的地址（生产者/消费者用）        |



### 2.7.5 消息确认/重试

| 配置项               | 默认值 | 说明               |
| -------------------- | ------ | ------------------ |
| `--max-req-timeout`  | 1h     | 消息最大请求超时   |
| `--max-message-size` | 1MB    | 最大消息字节数     |
| `--client-timeout`   | 60s    | TCP 客户端超时时间 |



### 2.7.6其它实用配置

| 配置项                  | 默认值 | 说明                       |
| ----------------------- | ------ | -------------------------- |
| `--queue-scan-interval` | 1s     | 扫描消息队列的时间间隔     |
| `--heap-profile`        | -      | Go 堆内存 profile 文件路径 |
| `--cpu-profile`         | -      | Go CPU profile 文件路径    |





# 第三章 示例代码



## 3.1 生产者

```go
// Instantiate a producer.
config := nsq.NewConfig()
producer, err := nsq.NewProducer("127.0.0.1:4150", config)
if err != nil {
	log.Fatal(err)
}

messageBody := []byte("hello")
topicName := "topic"

// Synchronously publish a single message to the specified topic.
// Messages can also be sent asynchronously and/or in batches.
err = producer.Publish(topicName, messageBody)
if err != nil {
	log.Fatal(err)
}

// Gracefully stop the producer when appropriate (e.g. before shutting down the service)
producer.Stop()
```



## 3.2 消费者

```go
package main
import (
	"log"
	"os/signal"
	"github.com/nsqio/go-nsq"
)

type myMessageHandler struct {}

// HandleMessage implements the Handler interface.
func (h *myMessageHandler) HandleMessage(m *nsq.Message) error {
	if len(m.Body) == 0 {
		// Returning nil will automatically send a FIN command to NSQ to mark the message as processed.
		// In this case, a message with an empty body is simply ignored/discarded.
		return nil
	}

	// do whatever actual message processing is desired
	err := processMessage(m.Body)

	// Returning a non-nil error will automatically send a REQ command to NSQ to re-queue the message.
	return err
}

func main() {
	// Instantiate a consumer that will subscribe to the provided channel.
	config := nsq.NewConfig()
	consumer, err := nsq.NewConsumer("topic", "channel", config)
	if err != nil {
		log.Fatal(err)
	}

	// Set the Handler for messages received by this Consumer. Can be called multiple times.
	// See also AddConcurrentHandlers.
	consumer.AddHandler(&myMessageHandler{})

	// Use nsqlookupd to discover nsqd instances.
	// See also ConnectToNSQD, ConnectToNSQDs, ConnectToNSQLookupds.
	err = consumer.ConnectToNSQLookupd("localhost:4161")
	if err != nil {
		log.Fatal(err)
	}

	// wait for signal to exit
	sigChan := make(chan os.Signal, 1)
	signal.Notify(sigChan, syscall.SIGINT, syscall.SIGTERM)
	<-sigChan

	// Gracefully stop the consumer.
	consumer.Stop()
}
```

