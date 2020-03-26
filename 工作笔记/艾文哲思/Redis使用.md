# 关闭保护模式

```shell
> config set protected-mode "no"
```





# 设置密码

```shell
CONFIG SET requirepass ${passwd}

# 示例
CONFIG SET requirepass tars2015
```



# 配置文件

1. 关闭保护模式

   > + protected-mode yes改为protected-mode no
   > + 注释bind 127.0.0.1
   
2. 指定配置文件启动redis

   ```shell
   redis-server /opt/redis/ect/redis.conf
   ```

   



# 连接服务器

```shell
redis-cli -h ${IP} -p ${PORT} -a ${PASSWD}

redis-cli -h 127.0.0.1 -p 6666 -a 123456
```





#  清空数据

1. FLUSHDB

   ```
   删除当前库中全部key
   ```

2. FLUSHALL

   ```
   删除全部库中的key
   ```



# 持久化配置

## RDB配置

```shell
# 数据保存在文件dump.rdb里,把这几行注释掉关闭RDB持久化

# 900秒内，如果超过1个key被修改，则发起快照保存
save 900 1

# 300秒内，如果超过10个key被修改，则发起快照保存
save 300 10

# 60秒内，如果1万个key被修改，则发起快照保存
save 60 10000
```

## AOF配置

```shell
# 开启AOF持久化,默认为no,开启后会产生一个appendonly.aof文件
appendonly yes
```





