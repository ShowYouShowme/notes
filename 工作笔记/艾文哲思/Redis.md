# 第一章 安装Redis服务



## 1.1 docker安装

```shell
docker pull redis:6.2.3

docker run -d -p 6379:6379 redis:6.2.3
```



## 1.2 yum安装

```shell
yum install -y epel-release
yum install redis -y

#启动redis
systemctl start redis
#设置开机启动
systemctl enable redis
```



## 1.3 源码安装

```shell
wget https://github.com/redis/redis/archive/refs/tags/3.2.12.tar.gz
tar -zxvf 3.2.12.tar.gz
cd redis-3.2.12/
make -j20
cd src/
# 安装,默认将可执行文件安装到/usr/local/bin; 需要自己copy配置文件到指定路径
make install

# 启动服务,前台启动;可以使用pm2来管理
./redis-server /path/to/redis.conf
```



# 第二章 安装C++开发库

## 2.1 下载文件

***

```shell
wget https://github.com/redis/hiredis/archive/v0.14.0.tar.gz
```

## 2.2 安装

***

```shell
tar -zxvf v0.14.0.tar.gz
cd ./hiredis-0.14.0/
make -j4
make PREFIX=/usr install   # 安装到指定目录,开发时直接能找到
ldconfig
ldconfig -v | grep hiredis # 不知道是否需要ldconfig,可以用此命令测试一下

# 如果第三方SDK 安装到/usr目录下依然找不到so(编译或者运行时),可以用命令
# ldconfig -v | grep hiredis 查看一下,或者试试 ldconfig 即可
```



# 第三章 Redis操作



## 3.1 关闭保护模式

当启用保护模式，而且没有密码时，服务器只接受来自IPv4地址(127.0.0.1)、IPv6地址(::1)或Unix套接字本地连接

***

```shell
> config set protected-mode "no"
```



## 3.2 设置密码

***

```shell

# 临时修改
CONFIG SET requirepass ${passwd}

# 示例
CONFIG SET requirepass tars2015


# 永久修改, 改配置文件redis.conf
requirepass jNu2yHNjMINN8cgH
```



## 3.3 配置文件

***

1. 关闭保护模式

   > + protected-mode yes改为protected-mode no
   > + 注释bind 127.0.0.1
   
2. 指定配置文件启动redis

   ```shell
   redis-server /opt/redis/ect/redis.conf
   ```

   



## 3.4 连接服务器

***

```shell
redis-cli -h ${IP} -p ${PORT} -a ${PASSWD}

redis-cli -h 127.0.0.1 -p 6666 -a 123456
```



##  3.5 清空数据

***

1. FLUSHDB

   ```
   删除当前库中全部key
   ```

2. FLUSHALL

   ```
   删除全部库中的key
   ```



## 3.6 持久化配置

***

### 3.6.1 RDB配置

```shell
# 数据保存在文件dump.rdb里,把这几行注释掉关闭RDB持久化

# 900秒内，如果超过1个key被修改，则发起快照保存
save 900 1

# 300秒内，如果超过10个key被修改，则发起快照保存
save 300 10

# 60秒内，如果1万个key被修改，则发起快照保存
save 60 10000
```

### 3.6.2 AOF配置

```shell
# 开启AOF持久化,默认为no,开启后会产生一个appendonly.aof文件
appendonly yes
```



### 3.6.3 混合持久化

```shell
#配置项  redis 4 以后才支持
aof-use-rdb-preamble yes

#触发重写AOF
bgwriteaof
```



## 3.7 非交互式执行命令

***

1. 列出键

   ```shell
   # 命令
   redis-cli -h ${host} -p ${port} -a ${passwd} ${cmd} 
   # 例子
   redis-cli -p 7111 KEYS '*'
   ```

2. 清空全部键

   ```shell
   redis-cli -p 7111 FLUSHALL
   ```

3. 订阅全部频道

   ```shell
   PSUBSCRIBE *
   ```

4. 发布消息：利用发布订阅，可以将redis作为配置中心，实时通知服务去更新配置！

   ```shell
   PUBLISH runoobChat "Redis PUBLISH test"
   ```

5. 退订全部频道

   ```shell
   PUNSUBSCRIBE *
   ```

6. 订阅给定的一个或多个频道

   ```shell
   SUBSCRIBE channel [channel ...]
   ```

7. 退订给定的一个或多个频道

   ```shell
   UNSUBSCRIBE channel [channel ...]
   ```

8. 查看帮助信息

   ```shell
   redis -h
   ```




## 3.8 关闭TCP监听,只用unix socket

```ini
port 0 
```

