# 第一章 安装Redis服务



## 1.1 docker安装

```shell
docker pull redis:6.2.3

docker run -d -p 6379:6379 redis:6.2.3
```



## 1.2 yum安装，版本太旧建议用新版本

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
# 对应golang的客户端是 "github.com/go-redis/redis/v8", v9连接会有错误信息
wget https://github.com/redis/redis/archive/refs/tags/7.0.0.tar.gz
tar -zxvf 7.0.0.tar.gz
yum install gcc gcc-c++
cd redis-7.0.0/
make 
# 安装,默认将可执行文件安装到/usr/local/bin; 需要自己copy配置文件到指定路径
mkdir -p /home/nash/app/redis
make PREFIX=/home/nash/app/redis/ install

cp redis.conf /home/nash/app/redis/
# 修改配置项
pidfile /var/run/redis_6379.pid
logfile "redis.log"
dir /home/nash/app/redis/data

save 900 1
save 300 10
save 60 10000
daemonize yes
bind 0.0.0.0
protected-mode no

# 启动服务
/home/nash/app/redis/bin/redis-server /home/nash/app/redis/redis.conf 

# 执行命令BGSAVE 可以在日志中看到信息
```



# 

# 第二章 Redis操作

## 3.0 重要配置项介绍

涉及到路径的配置

| 配置项             | 作用                    | 是否必须                | 是否包含路径   |
| ------------------ | ----------------------- | ----------------------- | -------------- |
| **dir**            | RDB/AOF 的目录          | 必须                    | 是（目录）     |
| **dbfilename**     | RDB 文件名              | 必须                    | 否（仅文件名） |
| **appendfilename** | AOF 文件名              | 可选（开启 AOF 时使用） | 否             |
| **logfile**        | 日志文件路径            | 可选                    | 是             |
| **pidfile**        | 守护模式下 PID 文件路径 | 可选                    | 是             |

### 3.0.1 dir（最重要）

指定 **RDB / AOF 文件保存的目录**。

```
dir /var/lib/redis/
```

所有以下文件都会放在这里：

- dump.rdb（RDB）
- appendonly.aof（AOF）
- Temp fork 文件
- 日志文件（如果是相对路径）

### 3.0.2 dbfilename

指定 **RDB 文件名**（仅文件名，不含路径）。

```
dbfilename dump.rdb
```

### 3.03 appendfilename

指定 **AOF 文件名**（仅文件名）。

```
appendfilename "appendonly.aof"
```

### 3.0.4 logfile（可选）

Redis 的日志文件路径。

```
logfile /var/log/redis/redis.log
```

如果配置为 **相对路径**，则相对 `dir`：

```
logfile redis.log   # 会写入 dir 目录
```

如果输出到 stdout，则使用：

```
logfile ""
```

### 3.0.5 pidfile（Daemon 模式需要）

Redis 以守护进程方式运行时的 PID 文件路径。

```
pidfile /var/run/redis_6379.pid
```



## 3.1 客户端

***

```shell
redis-cli -h ${IP} -p ${PORT} -a ${PASSWD}

redis-cli -h 127.0.0.1 -p 6666 -a 123456
```



## 3.2 持久化配置

***

### 3.2.1 RDB配置

```shell
# 数据保存在文件dump.rdb里,把这几行注释掉关闭RDB持久化

# 900秒内，如果超过1个key被修改，则发起快照保存
save 900 1

# 300秒内，如果超过10个key被修改，则发起快照保存
save 300 10

# 60秒内，如果1万个key被修改，则发起快照保存
save 60 10000
```

### 3.2.2 AOF配置

```shell
# 开启AOF持久化,默认为no,开启后会产生一个appendonly.aof文件
appendonly yes
```



### 3.2.3 混合持久化

```shell
#配置项  redis 4 以后才支持
aof-use-rdb-preamble yes

#触发重写AOF
bgwriteaof
```



## 3.3 配置项汇总



### 3.3.1 网络相关

| 配置项           | 默认值      | 说明                               |
| ---------------- | ----------- | ---------------------------------- |
| `bind`           | `127.0.0.1` | 监听的 IP 地址，可设置多个 IP      |
| `port`           | `6379`      | TCP 端口，客户端连接使用           |
| `tcp-backlog`    | `511`       | TCP 连接等待队列大小               |
| `timeout`        | `0`         | 客户端空闲超时秒数（0 表示不关闭） |
| `tcp-keepalive`  | `300`       | TCP keepalive 秒数，检测死连接     |
| `protected-mode` | `yes`       | 启动保护模式，只允许本地访问       |



### 3.3.2 持久化相关

RDB（快照持久化）

| 配置项       |   默认值   | 说明                              |
| ------------ | :--------: | --------------------------------- |
| `save`       |   900 1    | 触发快照的条件（秒数 + 变更次数） |
|              |   300 10   |                                   |
|              |  60 10000  |                                   |
| `dbfilename` | `dump.rdb` | RDB 文件名                        |
| `dir`        |    `./`    | RDB 文件保存路径                  |

AOF(追加文件持久化)

| 配置项                      | 默认值           | 说明                                     |
| --------------------------- | ---------------- | ---------------------------------------- |
| `appendonly`                | `no`             | 是否开启 AOF 持久化                      |
| `appendfilename`            | `appendonly.aof` | AOF 文件名                               |
| `appendfsync`               | `everysec`       | 写磁盘策略：`always` / `everysec` / `no` |
| `no-appendfsync-on-rewrite` | `yes`            | AOF 重写期间是否暂停 fsync               |



### 3.3.3 内存管理

| 配置项              | 默认值       | 说明                                                         |
| ------------------- | ------------ | ------------------------------------------------------------ |
| `maxmemory`         | `0`          | 最大内存，0 表示不限制                                       |
| `maxmemory-policy`  | `noeviction` | 内存达到上限时的淘汰策略（allkeys-lru、volatile-lru、allkeys-random 等） |
| `maxmemory-samples` | `5`          | LRU 策略采样数量，影响性能和精确度                           |



### 3.3.4 复制/集群相关

| 配置项                 | 默认值       | 说明                           |
| ---------------------- | ------------ | ------------------------------ |
| `slaveof`              | -            | 指定主节点 IP:端口，开启从节点 |
| `masterauth`           | -            | 从节点连接主节点的密码         |
| `cluster-enabled`      | `no`         | 是否开启 Redis Cluster 模式    |
| `cluster-config-file`  | `nodes.conf` | Cluster 配置文件               |
| `cluster-node-timeout` | `15000`      | 节点超时时间（毫秒）           |



### 3.3.5 安全相关

| 配置项           | 默认值 | 说明                                        |
| ---------------- | ------ | ------------------------------------------- |
| `requirepass`    | -      | 客户端连接密码                              |
| `rename-command` | -      | 重命名或禁用危险命令（如 FLUSHALL、CONFIG） |



### 3.3.6 日志和监控

| 配置项                    | 默认值           | 说明                                |
| ------------------------- | ---------------- | ----------------------------------- |
| `loglevel`                | `notice`         | 日志级别：debug/info/notice/warning |
| `logfile`                 | ""（控制台输出） | 日志文件路径                        |
| `databases`               | `16`             | 数据库数量                          |
| `slowlog-log-slower-than` | `10000`          | 慢查询日志阈值（微秒）              |
| `slowlog-max-len`         | `128`            | 保存慢查询条数上限                  |





### 3.3.7 优化建议

**高性能**：

- 开启 AOF `everysec` 或 RDB，避免 `always`
- 调整 `tcp-backlog` 和 `tcp-keepalive`

**内存控制**：

- 配置 `maxmemory` + `maxmemory-policy`

**安全**：

- 设置 `requirepass`
- 对危险命令使用 `rename-command`
