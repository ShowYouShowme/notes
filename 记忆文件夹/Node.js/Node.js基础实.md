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

> + 遇到异常时触发，如果未注册回调，会退出程序并输出错误信息。
>
> + 代码
>
>   ```javascript
>   import events = require('events');
>   let emitter = new events.EventEmitter();
>   emitter.emit('error');
>   ```

### 继承EventEmitter

***

1. 一般不会直接使用EventEmitter，而是在对象中继承
2. fs、net、http都是继承EventEmitter。





## 1-7 Stream

> 1. 定义：stream是个抽象接口，所有流对象都是EventEmitter的实例
>
> 2. 四种类型
>
>    > + Readable：可读操作
>    > + Writeable：可写操作
>    > + Duplex：可读可写操作
>    > + Transform：操作被写入数据，然后读出结果
>
> 3. 事件
>
>    > + data：有数据可读
>    > + end：没有更多数据可读
>    > + error：接收和写入过程中发生错误触发
>    > + finish：所有数据已被写入底层系统时触发

### 从流中读取数据

***

```javascript
import fs = require("fs");
let data : string = "";
let readStream = fs.createReadStream('input.txt');
readStream.setEncoding("utf8");
readStream.on("data",(chunk : any) : void=>{
    data += chunk;
});
readStream.on("end", ()=>{
   console.log(data);
});
readStream.on("error", (err : Error)=>{
    console.log(err.stack);
});
console.log("程序执行完毕!");
```

### 写入流

***

```javascript
import fs = require("fs");
let data : string = "我爱你,伟大的祖国!";
let writeStream = fs.createWriteStream('output.txt');
writeStream.write(data, 'utf8');
writeStream.end();
writeStream.on('finish', ():void=>{
   console.log("写入完成!");
});
writeStream.on('err', (err):void=>{
    console.log(err.stack);
});
console.log("程序执行完毕!");
```

### 管道流

***

+ 作用：从一个流中获取数据，并传递至另一个流中！

+ 示例

  ```javascript
  import fs = require("fs");
  let readStream : fs.ReadStream = fs.createReadStream('input.txt');
  let writeStream : fs.WriteStream = fs.createWriteStream("output.txt");
  //从readStream读取数据,然后写入到writeStream里面去
  readStream.pipe(writeStream);
  console.log("程序执行完毕!");
  ```

### 链式流

***

+ 定义：连接输出流到另外一个流，并创建多个流操作链的机制。一般用于管道操作！

+ 示例

  > 1. 压缩文件
  >
  >    ```javascript
  >    import fs   = require("fs");
  >    import zlib = require("zlib");
  >    fs.createReadStream('input.txt')
  >        .pipe(zlib.createGzip())
  >        .pipe(fs.createWriteStream('input.txt.gz'));
  >    console.log("程序执行完毕!");
  >    ```
  >
  > 2. 解压文件
  >
  >    ```javascript
  >    import fs   = require("fs");
  >    import zlib = require("zlib");
  >    fs.createReadStream('input.txt.gz')
  >    .pipe(zlib.createGunzip())
  >    .pipe(fs.createWriteStream('input2.txt'));
  >    console.log("文件解压完成!");
  >    ```





## 1-8 Buffer

+ 定义：存放二进制数据的缓冲区，类似一个整数数组

### 创建Buffer类

***

```javascript
let b1 : Buffer = new Buffer(10);
let b2 : Buffer = new Buffer([10, 20, 30, 40, 50]);
let b3 : Buffer = new Buffer("www.runoob.com", "utf-8");
```

### 写入缓冲区

***

```javascript
let buf : Buffer = new Buffer(10);
let len : number = buf.write("hello World!");
console.log("写入字节数:" + len);
```



### 从缓冲区读取数据

***

```javascript
let buf : Buffer = new Buffer(26);
for (let i : number = 0; i < 26; ++i){
    buf[i] = i + 97;
}
console.log(buf.toString('ascii'));
console.log(buf.toString('ascii', 0, 4));
```

### 将Buffer转换为JSON对象

***

```javascript
let buf : Buffer = new Buffer("i am BatMan");
let json : object = buf.toJSON();
console.log(json);
```

### 缓冲区合并

***

```javascript
let buf1 : Buffer = new Buffer("我的职业是");
let buf2 : Buffer = new Buffer("科学家");


let buf3 : Buffer = Buffer.concat([buf1, buf2]);

console.log("合并后的buf是:" + buf3.toString());
```

### 缓冲区比较

***

```javascript
let buf1 : Buffer = new Buffer("ABE");
let buf2 : Buffer = new Buffer("ABCD");

let result = buf1.compare(buf2);
if (result < 0){
    console.log(buf1 + "在" + buf2 + "之前!");
} else if(result == 0){
    console.log(buf1 + "与" + buf2 + "相同!");
}else{
    console.log(buf1 + "在" + buf2 + "之后!");
}
```

### 缓冲区裁剪

***

```javascript
let buf = new Buffer("ABCDEFHIJK");

let buf2 = buf.slice(1,3);

console.log(buf2.toString());
```

### 拷贝缓冲区

***

```javascript
// 与旧缓冲区指向同一块内存,只是索引不同
let buf = new Buffer("ABC");
let buf2 = new Buffer(3);
buf.copy(buf2);
console.log(buf2.toString());
```

### 缓冲区长度

***

```javascript
let buf : Buffer = new Buffer("1234567890");

console.log(buf.length)
```

### 方法参考手册

***

[Buffer文档](http://nodejs.cn/api/buffer.html)





## 1-9 模块系统

+ 定义：模块就是Node.JS代码文件

### 创建模块

***

> 1. hello.js
>
>    ```javascript
>    exports.world = ():void=>{
>        console.log("Hello World!");
>    }
>    ```
>
> 2. main.js
>
>    ```javascript
>    let hello = require("./hello");
>    hello.world();
>    ```

### 服务端模块

***

> + 模块分类
>
>   1. 原生模块(系统自带)
>   2. 自定义模块
>
> + 加载方式
>
>   1. 原生模块
>
>      ```javascript
>      let fs = require("fs");
>      ```
>
>   2. 自定义模块
>
>      ```javascript
>      //相对路径 == 推荐使用
>      let Hello = require("./hello");
>      //绝对路径 == 无法跨平台
>      let Hello = require("D:\\MyCode\\SayHeyToNode\\hello");
>      ```
>
> + 模块加载策略

