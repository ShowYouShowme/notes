# 第一章 搭建websocket服务

websocket 底层会处理TCP数据包的边界问题，用户收到的一定是一个完整的数据包，类似UDP协议

## 1.1 静态资源Http服务器

1. 创建文件夹

   ```shell
   mkdir htdocs
   ```

2. 启动http服务

   ```shell
   python -m http.server 8000
   ```

3. 编写html

   index.html

   ```html
   <!DOCTYPE html>
   <html lang="zh-CN">
   <head>
       <meta charset="utf-8">
       <meta http-equiv="X-UA-Compatible" content="IE=edge">
       <meta name="viewport" content="width=device-width, initial-scale=1">
       <title>Bootstrap 101 Template</title>
       <link href="bootstrap/css/bootstrap.css" rel="stylesheet">
       <script src="bootstrap/js/jquery.js"></script>
       <script src="bootstrap/js/bootstrap.js"></script>
   
   </head>
   <body>
       <div class="container-fluid">
           <button type="button" class="btn btn-success" id="connect">发起websocket连接</button>
           <input type="text" class="form-control" placeholder="输入发送的内容" id="send_content">
           <button type="button" class="btn btn-success" id="send">send</button>
       </div>
       <script>
           var ws = null;
           $("#connect").click(function (){
               ws = new WebSocket('ws://localhost:3000');
               ws.onopen = function () {
                   console.log('ws onopen');
               };
               ws.onmessage = function (e) {
                   console.log('from server: ' + e.data);
               };
           });
   
           $("#send").click(function (){
   
               let val = $("#send_content").val();
               ws.send(val);
               console.log("send msg:" + val);
           })
       </script>
   </body>
   </html>
   ```



## 1.2 编写websocket服务

1. 创建项目

   ```shell
   npm init
   ```

2. 安装ws包

   ```shell
   npm install ws
   
   #安装ts的声明文件,安装后可以使用import 导入
   npm i --save-dev @types/ws
   ```

3. 编写代码

   index.js

   ```javascript
   const WebSocket = require('ws');
   
   const wss = new WebSocket.Server({ port: 3000 });
   
   wss.on('connection', function connection(ws) {
   
       console.log("websocket 连接成功!");
       ws.on('message', function incoming(message) {
           console.log('received: %s', message);
           ws.send("返回数据:" + message);
       });
   });
   ```

4. websocket 客户端，配合protobuf

   ```shell
   import * as proto from "./cmd_net";
   import WebSocket from 'ws'
   // TODO 记录如何引入js的包
   // TODO 记录如何为js的包增加注释
   // import WebSocket = require("ws");
   
   let client = new WebSocket('ws://127.0.0.1:8080')
   
   function onOpen() {
       console.log("websocket connect successful!")
       let message: proto.TPackage = {}
       message.MainCmd = proto.MainCmdID.ACCOUNTS
       message.SubCmd = proto.SubCmdID.ACCOUNTS_TOKEN_LOGON_REQ
   
       let req: proto.CTokenLogonReq = {}
       req.GameID = 124
       req.Token = "a38cc710410e7119d6d869ac0356a659125b8ef6"
       message.Data = proto.encodeCTokenLogonReq(req)
       client.send(proto.encodeTPackage(message))
   }
   
   function onClose() {
   
   }
   
   function onMessage(data: any) {
       console.log(data)
       let message : proto.TPackage = proto.decodeTPackage(data)
       console.log(message.MainCmd, ":", message.SubCmd)
       let content : proto.CLogonSuccessResp = proto.decodeCLogonSuccessResp(message.Data as Uint8Array)
       console.log(JSON.stringify(content))
       console.log("finished...")
   }
   client.on("open", onOpen);
   client.on("close", onClose);
   client.on("message", onMessage);
   
   setInterval(()=>{
       console.log("....")
   }, 1000)
   ```

   





# 第二章 搭建socket.io服务



## 2.1 socket.io与websocket

socket.io在websocket的基础上包装了一层，因此websocket的客户端无法连接socket.io的服务。同样，socket.io的客户端也无法连接webocket的服务



## 2.2 客户端代码

index.html

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Bootstrap 101 Template</title>
    <link href="bootstrap/css/bootstrap.css" rel="stylesheet">
    <script src="bootstrap/js/jquery.js"></script>
    <script src="bootstrap/js/bootstrap.js"></script>
    <title>Socket.io Client</title>
    <script src="socket_io/socket.io.js"></script>
</head>
<body>

<div class="container-fluid">
    <button type="button" class="btn btn-success" id="connect">发起websocket连接</button>
    <input type="text" class="form-control" placeholder="输入发送的内容" id="send_content">
    <button type="button" class="btn btn-success" id="send">send</button>
</div>
<script>

    let socket = null;
    $("#connect").click(function (){
        socket = io("ws://localhost:3000");
        socket.on("connect", () => {
            // 等价于 socket.emit("message", "Hello"); 推荐全部用emit发送数据
            socket.send("Hello!");
            // 发送多个参数
            //socket.emit("salutations", "Hello!", { "mr": "john" }, Uint8Array.from([1, 2, 3, 4]));
        });

        // handle the event sent with socket.send()
        socket.on("message", data => {
            console.log("recv : " + data);
        });

        socket.on("typing",function (data){
            console.log("recv cmd typing from server, data : " + data);
        })

        socket.on("greetings", (elem1, elem2, elem3) => {
            console.log(elem1, elem2, elem3);
        });
    });

    $("#send").click(function (){
        let val = $("#send_content").val();
        socket.emit("typing", "justin bieber");
        console.log("send msg:" + val);
    })
</script>
</body>
</html>
```



## 2.3 服务代码

1. 安装依赖

   ```shell
   npm install socket.io
   ```

2. 示例代码

   ```javascript
   const server = require('http').createServer();
   const io = require('socket.io')(server,{ cors: true }); // 处理跨域请求
   io.on('connection', client => {
       console.log("有一个客户端连接进来!");
       client.on("message", (data) => {
           console.log("receive:" + data);
           client.send("receive:" + data);
       });
       client.on('typing', (data) => {
           console.log("client ask me to type:" + data);
           //client.emit("typing","who is your daddy!");
           client.emit("greetings", "Hey!", { "ms": "jane" }, Buffer.from([4, 3, 3, 1]));
       });
   });
   server.listen(3000);
   ```





## 2.4 相关api



### 2.4.1 发送消息

***

```javascript
// send to current request socket client
socket.emit('message', "this is a test");
 
// sending to all clients except sender
socket.broadcast.emit('message', "this is a test");
 
// sending to all clients in 'game' room(channel) except sender
socket.broadcast.to('game').emit('message', 'nice game');
 
// sending to all clients, include sender
io.sockets.emit('message', "this is a test");
 
// sending to all clients in 'game' room(channel), include sender
io.sockets.in('game').emit('message', 'cool game');
 
// sending to individual socketid
io.sockets.socket(socketid).emit('message', 'for your eyes only');
```