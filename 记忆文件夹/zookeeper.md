# 第一章 安装

zookeeper 是用java开发的中间件，因此必须要安装openjdk。

1. 安装openjdk1.8

   ```shell
   yum -y install java-1.8.0-openjdk java-1.8.0-openjdk-devel
   ```

   

2. 安装zk

   ```shell
   wget https://downloads.apache.org/zookeeper/stable/apache-zookeeper-3.8.4-bin.tar.gz
   tar -zxvf apache-zookeeper-3.8.4-bin.tar.gz
   mv apache-zookeeper-3.8.4-bin /usr/local/
   cd apache-zookeeper-3.8.4-bin/
   
   mkdir dataDir dataLogDir
   
   cd conf/
   cp zoo_sample.cfg zoo.cfg
   vim zoo.cfg
   # 增加两条配置
   dataDir=/usr/local/apache-zookeeper-3.8.4-bin/dataDir
   dataLogDir=/usr/local/apache-zookeeper-3.8.4-bin/dataLogDir
   
   # 配置环境变量
   vim /etc/profile
   export PATH=/usr/local/apache-zookeeper-3.8.4-bin/bin:$PATH
   
   # 启动服务
   zkServer.sh start
   
   # 停止服务
   zkServer.sh stop
   
   # 查看服务运行状态
   zkServer.sh status
   ```

   zk客户端

   ```shell
   # 启动客户端,并连接服务
   zkCli.sh
   
   # 常用命令
   0、列出节点信息
   ls ${path}
   
   1、创建节点
   create /rummy/provider
   
   # 创建临时节点,结束后删除
   create -e /rummy/tmp
   
   2、创建节点并且设置值
   create /rummy/provider 192.168.1.49:8890
   
   3、获取节点值
   get /rummy/provider 192.168.1.49:8890
   
   4、设置值
   set /rummy/provider 127.0.0.1:8880
   
   4、删除节点
   delete /rummy/provider 192.168.1.49:8890
   
   5、删除节点和子节点
   deleteall /rummy
   
   6、断开链接
   close
   
   7、链接
   connect
   
   8、退出客户端
   quit
   ```



示范代码

```go
// A simple exaple on how to use the package.
// Get, Children, Exist,
package main

import (
	"fmt"
	"time"

	"github.com/samuel/go-zookeeper/zk"
)

const (
	zkPath = "/rummy"
	zkNode = "192.168.1.210"
)

func getZnode(c *zk.Conn, path string) string {
	// Use `Get` to simply get data from ZK.
	// `Get` gets a string path, and return the data as []byte
	data, _, err := c.Get(path)
	if err != nil {
		panic(err)
	}
	// Transform the []byte into string
	s := string(data[:])
	return s
}

func setZNode(c *zk.Conn, path string, value string) {
	_, stat, err := c.Get(path)
	if err != nil {
		panic(err)
	}
	stat, err = c.Set(path, []byte(value), stat.Version)
	if err != nil {
		panic(err)
	}
}

func getChildren(c *zk.Conn, path string) []string {
	// Use `Children` to get a slice of strings with all the children of provided path.
	data, _, err := c.Children(zkPath)
	if err != nil {
		panic(err)
	}
	return data
}

func checkZnode(c *zk.Conn, path string) error {
	// Use `Exists` to check if zNode exist.
	// Retrun value is bool
	_, _, err := c.Exists(zkPath)
	return err
}

func main() {
	// Connect to ZK, print if there is an error, and close the connection at the end
	c, _, err := zk.Connect([]string{zkNode}, time.Second)
	defer c.Close()
	if err != nil {
		panic(err)
	}
	// Example #1
	// Just a simple Get
	// Get the data of spesific zNode
	myData := getZnode(c, zkPath)
	fmt.Printf("The data is: %v\n", myData)

	// Example #2
	// Get zNode Children and for each one of them,
	// check if the znode exist and then print the key and the data.
	myChld := getChildren(c, zkPath)
	fmt.Printf("The key are: %v\n", myChld)
	for _, key := range myChld {
		chldPath := zkPath + "/" + key
		err := checkZnode(c, chldPath)
		if err != nil {
			panic(err)
		}
		fmt.Printf("The key is: %v\n", key)
		fmt.Printf("The Data is: %v\n", getZnode(c, chldPath))
	}

	setZNode(c, zkPath, "newValue2")

	// Example #3
	// Set watch on znode, and wait for event.
	// Catch the event and use switch - case to do something, or just print the event name.
	data, _, ch, err := c.GetW(zkPath)
	if err != nil {
		panic(err)
	}
	fmt.Printf("The current data is: %v.\nI'm watching.\n", string(data[:]))
	for event := range ch {
		switch event.Type {
		case 1:
			fmt.Printf("Node created.")
			// Do somthing
		case 2:
			fmt.Printf("Node deleted!")
			// Do somthing
		case 3:
			fmt.Printf("Node changed.")
			// Do somthing
		case 4:
			fmt.Printf("Node children changed.")
			// Do somthing
		default:
			fmt.Printf("Something happen.")
		}
		// Or just ...
		fmt.Println(event.Type)

	}
}
```





# 第二章 应用场景

可以用来管理全部的配置项目。



## 2.1 配置中心

1. 发布者将数据发布到ZK节点上，供订阅者动态获取数据，实现配置信息的集中式管理和动态更新。
2. 应用在启动的时候会主动来获取一次配置，同时，在节点上注册一个 Watcher，这样一来，以后每次配置有更新的时候，都会实时通知到订阅的客户端，从而达到获取最新配置信息的目的



## 2.2 负载均衡

上游服务启动时，把地址信息注册到zk。网关收到客户端请求时，获取zk对应服务的列表，然后轮询转发！因此，网关可以使用grpc + zookeeper 来替代 rabbitmq



## 2.3 命名服务

上游服务之间rpc调用时，可以通过服务名 获取服务器的地址，然后发起rpc请求，这样就不需要频繁更改配置了。





