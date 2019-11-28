## 1-2 创建应用

### node.js运行原理

***

php开发时，接受http请求并提供web页面由apache或nginx来处理，php仅处理业务。Node.js不仅处理业务，还实现了整个http服务器。



### 创建应用

***

```typescript
import http = require("http");

let server = http.createServer((req: http.IncomingMessage, res: http.ServerResponse) : void=>{
    res.writeHead(200,{'Content-Type':'text/plain'});
    res.end('Hello World!\n');
});

server.listen(8899,'0.0.0.0');
```



## 1-3 REPL

### 定义

***

Node.js的交互式解释器



### 简单示范

***

> 1. 表达式运算
>
> 2. 使用变量
>
> 3. 多行表达式
>
> 4. 下划线变量
>
>    ```javascript
>    > var x=10
>    > var y=30
>    > x+y
>    > var sum=_
>    > console.log(sum)
>    ```



### 常用的REPL命令

***

> 1. ctrl+c：退出当前终端
> 2. ctrl+c：按下两次，退出Node REPL
> 3. ctrl+d：退出Node REPL
> 4. 上/下方向键：查看历史命令
> 5. tab键：列出当前命令
> 6. help：列出使用命令
> 7. break：退出多行表达式
> 8. clear：退出多行表达式
> 9. save filename：保存当前的Node REPL
> 10. load filename：载入当前Node REPL会话的文件内容



## 1-4 回调函数

### 回调函数的机制原理

***

任务开始执行前注册回调函数，任务执行完毕执行回调函数！

### 简单范例

***

> 1. 阻塞代码
>
>    ```javascript
>    import fs = require("fs");
>    let data : Buffer = fs.readFileSync("input.txt");
>    console.log(data.toString());
>    console.log("程序执行完毕!");
>    ```
>
>    
>
> 2. 非阻塞代码
>
>    ```javascript
>    import fs = require("fs");
>    fs.readFile("input.txt",(err: NodeJS.ErrnoException | null, data: Buffer)=>{
>        if(err){
>            return console.error(err);
>        }else{
>            console.log(data.toString());
>        }
>    })
>    console.log("程序执行完毕!");
>    ```
>



## 1-5 事件循环

### 事件循环机制解释

***

基于观察者模式实现，有一个while事件主循环，类似Libevent，直到没有事件观察者就退出！

### 事件驱动程序

***

Node.js事件驱动模型中，有一个主循环监听事件，事件发生时触发回调函数。我们把它成为事件IO或非阻塞IO。

### 简单范例

***

```javascript
import event = require("events");
let eventEmitter = new event.EventEmitter();
let connectHandler = function connected() {
    console.log("链接成功!");

    eventEmitter.emit("date_received");
};
eventEmitter.on("connection", connectHandler);
eventEmitter.on("date_received", ()=>{
    console.log("数据接受成功!");
});
eventEmitter.emit("connection");
console.log("程序执行完毕!");
```



### Node应用程序如何工作

***

在Node应用中，执行异步操作的函数将回调函数作为最后一个参数。回调函数接收**错误对象作为第一个参数**。

```javascript
import fs = require("fs");
fs.readFile('input.txt',(err: NodeJS.ErrnoException | null, data: Buffer) : void=>{
   if (err){
       console.log(err.stack);
       return;
   }
   console.log(data.toString());
});
console.log("程序执行完毕!");
```





## 1-6 EventEmitter

### EventEmitter类

***

1. 所有产生事件的对象都是events.EventEmitter的实例

2. 所有异步I/O操作在完成时送一个事件到事件队列。

3. EventEmitter对象如果实例化时出错，则会触发error事件

4. 添加新的监听器时，触发newListener事件；监听器被移除时，removeListener事件被触发。

5. 代码示例

   ```javascript
   import Event = require("events");
   let event = new Event.EventEmitter();
   event.on('some_event',():void=>{
       console.log("some_event事件触发!");
   });
   setTimeout(():void=>{
       event.emit("some_event");
   }, 3000);
   ```

### EventEmitter常用方法

***

1. 代码

   ```javascript
   import Event = require("events");
   let event = new Event.EventEmitter();
   event.on("someEvent", (...args: any[]) : void=>{
       console.log("listen1", args[0], args[1]);
   });
   event.on("someEvent", (...args: any[]) : void=>{
       console.log("listen2", args[0], args[1]);
   });
   event.emit("someEvent","参数1", "参数2");
   ```

   ```javascript
   import Event = require("events");
   let event = new Event.EventEmitter();
   let f1 = ():void=>{
       console.log("监听器1执行!");
   };
   let f2 = ():void=>{
       console.log("监听器2执行!");
   };
   //绑定connection事件
   event.addListener('connection', f1);
   event.on('connection', f2);
   //获取监听器数量
   let count : number = Event.EventEmitter.listenerCount(event, "connection");
   console.log(count + "个监听器!");
   event.emit("connection");
   event.removeListener("connection", f1);
   console.log("f1 不再监听!");
   event.emit("connection");
   count = Event.EventEmitter.listenerCount(event, "connection");
   console.log(count + "个监听器!");
   console.log("finished!");
   ```

2. 常用方法

   > 1. [emitter.addListener(eventName, listener)](http://nodejs.cn/api/events.html#events_emitter_addlistener_eventname_listener)
   >
   > 2. [emitter.on(eventName, listener)](http://nodejs.cn/api/events.html#events_emitter_on_eventname_listener)
   >
   > 3. [emitter.once(eventName, listener)](http://nodejs.cn/api/events.html#events_emitter_once_eventname_listener)
   >
   > 4. [emitter.removeListener(eventName, listener)](http://nodejs.cn/api/events.html#events_emitter_removelistener_eventname_listener)
   >
   > 5. [emitter.removeAllListeners([eventName\])](http://nodejs.cn/api/events.html#events_emitter_removealllisteners_eventname)
   >
   > 6. [emitter.setMaxListeners(n)](http://nodejs.cn/api/events.html#events_emitter_setmaxlisteners_n)
   >
   > 7. [emitter.listeners(eventName)](http://nodejs.cn/api/events.html#events_emitter_listeners_eventname)
   >
   > 8. [emitter.emit(eventName[, ...args\])](http://nodejs.cn/api/events.html#events_emitter_emit_eventname_args)
   >
   > 9. emitter.listenerCount

### error事件

***



### 继承EventEmitter

***

