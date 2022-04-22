# 第一章 配置



## 1.1 单节点网络

```shell
harbor = 0
standalone = nil
```



## 1.2 多节点网络



### 1.2.1 参数说明

>  harbor
> 节点唯一性编号，1~255 之间的任意整数，因此一个 skynet 网络最多支持 255 个节点。
> 若某个 slave 意外退出，则对应的 harbor 会被废弃，不可再使用（即使该 slave 后续重启），这样是为了防止网络中其它服务还持有这个断开的 slave 上的服务地址，而一个新的进程以相同的 harbor 接入时，是无法保证旧地址和新地址不重复的。也就是说该模式下，已经用过的 harbor 无法再次使用，所以该模式不能实现热切换，而只能充当单个物理机压力的分担。
>
>  standalone
> slave 节点指定为 nil，master 需要配置该选项（控制中心的地址和端口），表示这个进程是 master，它会监听这个地址并等待其它节点接入。
>
>  master
> 指定 skynet 控制中心的地址和端口，与 master 节点 standalone 项相同，slave 会尝试连接这个地址。
>
>  address
> 当前 skynet 节点的地址和端口，方便其它节点和它组网，master 会通过（harbor 和 address）区分不同的 slave。





### 1.2.2 配置样例

+ master

  ```shell
  harbor = 1
  standalone = "192.168.255.128:20003"
  master = "192.168.255.128:20003"
  address = "192.168.255.128:30001"
  ```

+ slave

  ```shell
  harbor= 2
  standalone = nil
  master = "192.168.255.128:20003"
  address = "192.168.255.128:30002"
  ```

  