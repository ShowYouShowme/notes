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




# 第二章 网络编程



## 2.1 常用api

```lua
--这样就能够在你的服务中引入这组 api 。
local socket = require "skynet.socket"
​
--创建一个 TCP 链接。返回一个数字 id 。
socket.open(address, port)    
​
--关闭一个链接，这个 API 有可能阻塞住执行流。由于若是有其它 coroutine 
--正在阻塞读这个 id 对应的链接，会先驱使读操做结束，close 操做才返回。
socket.close(id)
​
--在极其罕见的状况下，须要粗暴的直接关闭某个链接，而避免 socket.close 的阻塞等待流程，可使用它。
socket.close_fd(id)
​
--强行关闭一个链接。和 close 不一样的是，它不会等待可能存在的其它 coroutine 的读操做。
--通常不建议使用这个 API ，但若是你须要在 __gc 元方法中关闭链接的话，
--shutdown 是一个比 close 更好的选择（由于在 gc 过程当中没法切换 coroutine）。与close_fd相似
socket.shutdown(id)
​
--[[
 从一个 socket 上读 sz 指定的字节数。
 若是读到了指定长度的字符串，它把这个字符串返回。
 若是链接断开致使字节数不够，将返回一个 false 加上读到的字符串。
 若是 sz 为 nil ，则返回尽量多的字节数，但至少读一个字节（若无新数据，会阻塞）。
--]]
socket.read(id, sz)
​
--从一个 socket 上读全部的数据，直到 socket 主动断开，或在其它 coroutine 用 socket.close 关闭它。
socket.readall(id)
​
--从一个 socket 上读一行数据。sep 指行分割符。默认的 sep 为 "\n"。读到的字符串是不包含这个分割符的。
--若是另一端就关闭了，那么这个时候会返回一个nil，若是buffer中有未读数据则做为第二个返回值返回。
socket.readline(id, sep) 
​
--等待一个 socket 可读。
socket.block(id) 
​
 
--把一个字符串置入正常的写队列，skynet 框架会在 socket 可写时发送它。
socket.write(id, str) 
​
--把字符串写入低优先级队列。若是正常的写队列还有写操做未完成时，低优先级队列上的数据永远不会被发出。
--只有在正常写队列为空时，才会处理低优先级队列。可是，每次写的字符串均可以当作原子操做。
--不会只发送一半，而后转去发送正常写队列的数据。
socket.lwrite(id, str) 
​
--监听一个端口，返回一个 id ，供 start 使用。
socket.listen(address, port) 
​
--[[
 accept 是一个函数。每当一个监听的 id 对应的 socket 上有链接接入的时候，都会调用 accept 函数。
这个函数会获得接入链接的 id 以及 ip 地址。你能够作后续操做。
 每当 accept 函数得到一个新的 socket id 后，并不会当即收到这个 socket 上的数据。
这是由于，咱们有时会但愿把这个 socket 的操做权转让给别的服务去处理。accept(id, addr)
]]--
socket.start(id , accept) 
​
--[[
 任何一个服务只有在调用 socket.start(id) 以后，才能够读到这个 socket 上的数据。
向一个 socket id 写数据也须要先调用 start 。
 socket 的 id 对于整个 skynet 节点都是公开的。也就是说，你能够把 id 这个数字
经过消息发送给其它服务，其余服务也能够去操做它。skynet 框架是根据调用 start 这个 
api 的位置来决定把对应 socket 上的数据转发到哪里去的。
--]]
socket.start(id)
​
--清除 socket id 在本服务内的数据结构，但并不关闭这个 socket 。
--这能够用于你把 id 发送给其它服务，以转交 socket 的控制权。
socket.abandon(id) 
​
--[[
 当 id 对应的 socket 上待发的数据超过 1M 字节后，系统将回调 callback 以示警告。
function callback(id, size) 回调函数接收两个参数 id 和 size ，size 的单位是 K 。
 若是你不设回调，那么将每增长 64K 利用 skynet.error 写一行错误信息。
--]]
socket.warning(id, callback) 
```



## 2.2 Tcp服务端

```lua
local skynet    = require "skynet"
local socket    = require "skynet.socket"
​
--简单echo服务
function echo(cID, addr)
    socket.start(cID)
    while true do
        local str = socket.read(cID)
        if str then
            skynet.error("recv " ..str)
            socket.write(cID, string.upper(str))
        else
            socket.close(cID)
            skynet.error(addr .. " disconnect")
            return
        end
    end
end
​
function accept(cID, addr)
   skynet.error(addr .. " accepted")
    skynet.fork(echo, cID, addr) --来一个链接，就开一个新的协程来处理客户端数据
end
​
--服务入口
skynet.start(function()
    local addr = "0.0.0.0:8001"
    skynet.error("listen " .. addr)
    local lID = socket.listen(addr)
    assert(lID)
    socket.start(lID, accept)
end)
```



## 2.3 socket.readline

```lua
local skynet    = require "skynet"
local socket    = require "skynet.socket"
​
--简单echo服务
function echo(cID, addr)
    socket.start(cID)
    while true do
     local str, endstr = socket.readline(cID)
        --local str, endstr = socket.readline(cID, "\n")
        if str then
            skynet.error("recv " ..str)
            socket.write(cID, string.upper(str))
        else
            socket.close(cID)
      if endstr then
       skynet.error("last recv " ..endstr)
      end
            skynet.error(addr .. " disconnect")
            return
        end
    end
end
​
function accept(cID, addr)
   skynet.error(addr .. " accepted")
    skynet.fork(echo, cID, addr)
end
​
--服务入口
skynet.start(function()
    local addr = "0.0.0.0:8001"
    skynet.error("listen " .. addr)
    local lID = socket.listen(addr)
    assert(lID)
    socket.start(lID, accept)
end)
```



## 2.4 socket.readall

```lua
local skynet    = require "skynet"
local socket    = require "skynet.socket"
​
--简单echo服务
function echo(cID, addr)
    socket.start(cID)
 local str = socket.readall(cID)
    if str then
       skynet.error("recv " ..str)
    end 
    skynet.error(addr .. " close")
    socket.close(cID)
    return
end
​
function accept(cID, addr)
   skynet.error(addr .. " accepted")
    skynet.fork(echo, cID, addr)
end
​
--服务入口
skynet.start(function()
    local addr = "0.0.0.0:8001"
    skynet.error("listen " .. addr)
    local lID = socket.listen(addr)
    assert(lID)
    socket.start(lID, accept)
end)
```



## 2.5 低优先级发送函数

```lua
local skynet    = require "skynet"
local socket    = require "skynet.socket"
​
--简单echo服务
function echo(cID, addr)
    socket.start(cID)
    while true do
        local str = socket.read(cID)
        if str then
            skynet.error("recv " ..str)
        --因为cpu处理很是快，没法看到效果，只有当cpu复核太高的时候，才会出现低优先级后发送的现象
      socket.lwrite(cID, "l:" .. string.upper(str))  
            socket.write(cID, "h:" .. string.upper(str))  
        else
            socket.close(cID)
            skynet.error(addr .. " disconnect")
            return
        end
    end
end
​
function accept(cID, addr)
   skynet.error(addr .. " accepted")
    --若是不开协程，那么同一时刻确定只能处理一个客户端的链接请求
    skynet.fork(echo, cID, addr)   
end
​
--服务入口
skynet.start(function()
    local addr = "0.0.0.0:8001"
    skynet.error("listen " .. addr)
    local lID = socket.listen(addr)
    assert(lID)
    socket.start(lID, accept)
end)
```



## 2.6 socket代理服务

```lua
-- socketlisten.lua
local skynet    = require "skynet"
local socket    = require "skynet.socket"
skynet.start(function()
    local addr = "0.0.0.0:8001"
    skynet.error("listen " .. addr)
    local lID = socket.listen(addr)
    assert(lID)
    socket.start(lID , function(cID, addr)
        skynet.error(addr .. " accepted")
        skynet.newservice("socketagent", cID, addr)
    end)
end)
```

```lua
-- socketagent.lua
local skynet    = require "skynet"
local socket    = require "skynet.socket"
function echo(cID, addr)
    socket.start(cID)
    while true do
        local str = socket.read(cID)
        if str then
            skynet.error("recv " ..str)
            socket.write(cID, string.upper(str))  
        else
            socket.close(cID)
            skynet.error(addr .. " disconnect")
            return
        end
    end
end
​
local cID, addr = ...
cID = tonumber(cID)
​
skynet.start(function()
    skynet.fork(function()
        echo(cID, addr)
        skynet.exit()
    end)
end)
```



## 2.7 转交socket控制权

```lua
local skynet    = require "skynet"
local socket    = require "skynet.socket"
skynet.start(function()
    local addr = "0.0.0.0:8001"
    skynet.error("listen " .. addr)
    local lID = socket.listen(addr)
    assert(lID)
    socket.start(lID , function(cID, addr)
        skynet.error(addr .. " accepted")
  --当前服务开始使用套接字
  socket.start(cID)
  local str = socket.read(cID)
  if(str) then
   socket.write(cID, string.upper(str))
  end
        --不想使用了，这个时候遗弃控制权
  socket.abandon(cID) 
​
        skynet.newservice("socketagent", cID, addr) --代理服务不变
    end)
end)
```



## 2.8 Tcp客户端

```lua
-- socketclient.lua
local skynet    = require "skynet"
local socket    = require "skynet.socket"
​
function client(id)
  local i = 0
  while(i < 3) do
     skynet.error("send data"..i)
     socket.write(id, "data"..i.."\n")
     local str = socket.readline(id)
     if str then
         skynet.error("recv " .. str)
     else
         skynet.error("disconnect")
     end
     i = i + 1
   end
   socket.close(id)   --不主动关闭也行，服务退出的时候，会自动将套接字关闭
   skynet.exit()
end
​
skynet.start(function()
    local addr = "127.0.0.1:8001"
    skynet.error("connect ".. addr)
    local id  = socket.open(addr)
    assert(id)
    --启动读协程
    skynet.fork(client, id)
end)
```

```lua
-- serverreadline.lua 监听端代码
local skynet    = require "skynet"
local socket    = require "skynet.socket"
​
--简单echo服务
function echo(cID, addr)
    socket.start(cID)
    while true do
        local str = socket.readline(cID)
        if str then
        skynet.fork(function()
             skynet.error("recv " ..str)
       skynet.sleep(math.random(1, 5) * 100)
       socket.write(cID, string.upper(str) .. "\n")
         end)
        else
            socket.close(cID)
            skynet.error(addr .. " disconnect")
            return
        end
    end
end
​
function accept(cID, addr)
   skynet.error(addr .. " accepted")
    skynet.fork(echo, cID, addr)
end
​
--服务入口
skynet.start(function()
    local addr = "0.0.0.0:8001"
    skynet.error("listen " .. addr)
    local lID = socket.listen(addr)
    assert(lID)
    socket.start(lID, accept)
end)
```



## 2.9 发请求与收应答分离

```lua
local skynet    = require "skynet"
local socket    = require "skynet.socket"
​
local function recv(id)
   local i = 0
   while(i < 3) do
    local str = socket.readline(id)
    if str then
         skynet.error("recv " .. str)
    else
         skynet.error("disconnect")
    end
 i = i + 1
   end
   socket.close(id)       --未接收完不要关闭
   skynet.exit()
end
​
local function send(id)    --不用管有没接受到数据直接发送三次
    local i = 0
    while(i < 3) do
    skynet.error("send data"..i)
    socket.write(id, "data"..i.."\n")
     i = i + 1
    end
end
​
skynet.start(function()
    local addr = "127.0.0.1:8001"
    skynet.error("connect ".. addr)
    local id  = socket.open(addr)
    assert(id)
    --启动读协程
    skynet.fork(recv, id)
    --启动写协程
    skynet.fork(send, id)
end)
```

