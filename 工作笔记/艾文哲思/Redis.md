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

***

```shell
> config set protected-mode "no"
```



## 3.2 设置密码

***

```shell
CONFIG SET requirepass ${passwd}

# 示例
CONFIG SET requirepass tars2015
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

4. 退订全部频道

   ```shell
   PUNSUBSCRIBE *
   ```

5. 订阅给定的一个或多个频道

   ```shell
   SUBSCRIBE channel [channel ...]
   ```

6. 退订给定的一个或多个频道

   ```shell
   UNSUBSCRIBE channel [channel ...]
   ```

7. 查看帮助信息

   ```shell
   redis -h
   ```

   
