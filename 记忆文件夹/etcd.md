# 第一章 安装

```shell
sudo yum install -y etcd

# 增加配置
sudo vim /etc/profile
export ETCDCTL_API=3
```





# 第二章 常见命令



## 2.1 基本key-value操作

| 命令  | 用法                            | 说明                   |
| ----- | ------------------------------- | ---------------------- |
| `put` | `etcdctl put <key> <value>`     | 写入或更新 key         |
| `get` | `etcdctl get <key>`             | 查询 key 的值          |
| `get` | `etcdctl get <prefix> --prefix` | 查询指定前缀的所有 key |
| `del` | `etcdctl del <key>`             | 删除 key               |
| `del` | `etcdctl del <prefix> --prefix` | 删除指定前缀的所有 key |

示例

```ini
[put]
;设定某个key的值
etcdctl put /app/config "version1"

[get]
;获取某个key的值
etcdctl get /app/config
etcdctl get /testdir/testkey /testdir/testkey3
; 获取某个前缀的所有键值对
etcdctl get /app --prefix
; 限制获取的数量
etcdctl get --prefix --limit=2 /testdir/testkey

[del]
;del 删除某个key的值
etcdctl del /app/config
etcdctl del foo foo9
;删除并返回 key value
etcdctl del --prev-kv zoo
;删除前缀为 zoo 的键
etcdctl del --prefix zoo
```



## 2.2 Lease(租约)相关

用于管理 key 的 TTL（过期时间）。

| 命令               | 用法                                 | 说明                        |
| ------------------ | ------------------------------------ | --------------------------- |
| `lease grant`      | `etcdctl lease grant <TTL秒>`        | 创建一个租约                |
| `lease revoke`     | `etcdctl lease revoke <leaseID>`     | 撤销租约，关联 key 会被删除 |
| `lease keep-alive` | `etcdctl lease keep-alive <leaseID>` | 手动续约租约                |
| `lease timetolive` | `etcdctl lease timetolive <leaseID>` | 查看租约剩余 TTL            |

示例

```ini
;创建租约
[nash@WhiteHouse ~]$ etcdctl lease grant 60
lease 694d9b030032ca68 granted with TTL(60s)

;绑定                                  <key>          <value> 
etcdctl put --lease=694d9b030032ca68 /game/user/1001 6000

;查看租约剩余时间
etcdctl lease timetolive 694d9b030032ca68

;续约
etcdctl lease keep-alive 694d9b030032ca68

;撤销租约
etcdctl lease revoke 694d9b030032ca68
```



## 2.3 事务操作

   | 命令           | 用法          | 说明                            |
   | -------------- | ------------- | ------------------------------- |
   | `txn`          | `etcdctl txn` | 执行条件 + Then + Else 原子操作 |
   | 事务命令示例： |               |                                 |

   ```shell
   etcdctl txn << EOF
   compare
     version("/lock/game") = "0"
   then
     put /lock/game "locked"
   else
     get /lock/game
   EOF
   ```



## 2.4 监控

| 命令    | 用法                  | 说明     |
| ------- | --------------------- | -------- |
| `watch` | `etcdctl watch <key>` | 监控变化 |

```
etcdctl watch /game/user/2002
```





## 2.5 golang实现分布式锁

```go
import (
    "context"
    "time"
    clientv3 "go.etcd.io/etcd/client/v3"
    "go.etcd.io/etcd/client/v3/concurrency"
)

func main() {
    cli, _ := clientv3.New(clientv3.Config{
        Endpoints: []string{"localhost:2379"},
        DialTimeout: 5 * time.Second,
    })
    defer cli.Close()

    // 创建一个会话（基于租约）,客户端如果断开,当租约过期后就自动解锁
    sess, _ := concurrency.NewSession(cli, concurrency.WithTTL(10))
    defer sess.Close()

    // 创建分布式锁
    mutex := concurrency.NewMutex(sess, "/game/user/1001")

    // 获取锁
    if err := mutex.Lock(context.Background()); err != nil {
        panic(err)
    }

    // 临界区
    println("获得锁，可以执行操作")

    // 释放锁
    if err := mutex.Unlock(context.Background()); err != nil {
        panic(err)
    }
}

```

