## 1-1 前言

### 创建项目

1. 初始化npm包管理器

   ```shell
   npm init
   ```

2. 创建项目配置文件

   ```shell
   # 安装 npm install -g typescript
   
   tsc --init
   ```

3. 修改项目配置

   ```shell
   "sourceMap": true,
   "outDir": "./bin",
   "allowJs": true,
   "target": "es6",
   ```

### 调试项目

1. 编译生成javascript代码

   ```shell
   tsc
   ```

2. 断点调试

   > 1. webstorm
   >
   > 在ts代码里面打断点，然后启动bin目录下生成的js文件即可
   >
   > 2. vscode
   >
   > 添加debug配置，然后设置启动的js文件，最后断点启动项目即可
### 代码跳转

***

> 部分符号，比如函数跳转不正常，先执行断点下来，再跳转即可！



### 第三方包安装

#### redis安装

------

1. 普通redis

   ```shell
   npm install redis --save
   
   # 安装声明文件
   npm install @types/redis
   ```

2. ioredis：可以直接await操作

   ```shell
   npm install ioredis
   
   # 安装声明文件
   npm install @types/ioredis
   ```

#### MySQL安装

------

1. 普通MySQL

   ```shell
   npm install mysql --save
   
   # 安装声明文件
   npm install @types/mysql
   ```

2. typeorm

   ```shell
   npm install typeorm 
   ```

3. sequelize

   ```shell
   npm install sequelize
   ```

#### typescript安装

------

```shell
npm install typescript -g
```

#### 安装node声明文件

------

```shell
npm install @types/node
```

### npm教程

1. 配置代理

   ```shell
   npm config set proxy=http://127.0.0.1:8090
   ```

2. 全局安装

   ```shell
   npm install ${包名} -g
   ```

3. 安装

   ```shell
   npm install ${包名}
   
   # 安装指定版本的包
   npm install ${包名}@${version}
   # 例子
   npm install  gulp@3.9.1
   ```

4. 卸载

   ```shell
   npm uninstall ${包名}
   ```

5. 更新

   ```shell
   npm update ${包名}
   ```

6. 检查包是否过时

   ```shell
   npm outdated
   ```

7. 列出安装的全部包

   ```shell
   npm ls
   ```

8. 参数说明

   > 1. --save 或者-S
   >
   > ```shell
   > # 安装模块后，模块的名称将加入到dependencies（生产阶段的依赖）
   > npm install gulp --save 或 npm install gulp –S
   > 
   > # package.json内容
   > "dependencies": {
   >     "gulp": "^3.9.1"
   > }
   > ```
   >
   > 2. --save-dev 或者-D
   >
   > ```shell
   > # 安装模块后，模块名称将加入到devDependencies（开发阶段的依赖）
   > npm install gulp --save-dev 或 npm install gulp –D
   > 
   > # package.json 的devDependencies属性：
   > "devDependencies": {
   > 
   >     "gulp": "^3.9.1"
   > 
   > }
   > ```
   >
   > 3. --save-optional 或者-O
   >
   > ```shell
   > # 安装模块后，模块名称将加入到optionalDependencies（可选阶段的依赖）
   > npm install gulp --save-optional 或 npm install gulp -O
   > 
   > # package.json 文件的optionalDependencies属性：
   > "optionalDependencies": {
   > 
   >     "gulp": "^3.9.1"
   > 
   >        }
   > ```
   >
   > 4. --save-exact 或者 -E 
   >
   > ```shell
   > # 精确安装指定模块版本
   > npm install gulp-concat --save-exact 或 npm install gulp-concat –E
   > 
   > # package.json文件里"dependencies"属性的
   > 
   > "dependencies": {
   > 
   >     "gulp-concat": "2.6.1"   //注意此处：版本号没有 ^
   > 
   > }
   > ```
   >
   > 

### 示例代码

```js
import redis = require('redis') //引入nodejs的包
import http =  require('http')

let port : number = 6379;
let host : string = "0.0.0.0";

let client : redis.RedisClient = redis.createClient(port, host);


let server:http.Server = http.createServer((req: http.IncomingMessage, res: http.ServerResponse):void =>{
    console.log("data comming!");
});

server.listen( 9999, "0.0.0.0" );
```





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
> let fd : number = fs.openSync("configureNet.bat", "r");
> let data : Buffer = Buffer.alloc(1024);
> fs.readSync(fd, data, 0,1024,0);
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

> 1. hello.ts
>
> ```javascript
> // 属性和方法默认为public
> export class Hello{
>     name : string = "";
>     constructor(){}
>     public setName(thyName : string){
>         this.name = thyName;
>     }
> 
>     public sayHello(){
>         console.log("Hello" + this.name);
>     }
> }
> 
> export function world(){
>     console.log("Hello World!");
> }
> ```
>
> 2. main.ts
>
> ```javascript
> import {Hello, world} from './hello'
> 
> let hello = new Hello();
> 
> hello.setName("wzc");
> hello.sayHello();
> world();
> ```

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
> + 模块加载策略[了解]





## 1-10 函数

### 创建函数

***

```javascript
function printOut(content : string) {
    console.log(content)
}

function execute(fun : (param : string)=>void, value : string) {
    fun(value);
}
execute(printOut, "Hello Function!");
```



### 匿名函数

***

```javascript
function nodeFun(fun : (param : string)=>void, value : string) {
    fun(value);
}

nodeFun((param : string) : void =>{
    console.log("param:" + param);
}, "Hello second Function!")
```



### 函数传递的工作原理

***

```javascript
import http = require("http");

let host : string = "0.0.0.0";
let port : number = 8888;
let server : http.Server = http.createServer((req: IncomingMessage, res: ServerResponse) : void=>{
    res.writeHead(200, {"content-Type":"text/plain"});
    res.write("Hello function!");
    res.end();
});

server.listen(port, host);
```



## 1-11 路由

+ 定义：访问路径

  > 获取请求的URL和GET/POST参数，然后执行相应的代码。所有的数据都在request对象当中

+ 路由定义

  ```javascript
  import http = require("http");
  import url  = require("url");
  import fs   = require("fs");
  
  let host : string   = "0.0.0.0";
  let port : number   = 8888;
  function handler(req: IncomingMessage, res: ServerResponse) : void{
      let pathName : string = url.parse(<string>req.url).pathname as string;
      console.log("Request for " + pathName + " receive!");
  
      function showPage(path : string, status : number) {
          let content : Buffer = fs.readFileSync(path);
          res.writeHead(status, {"Content-Type":"text/html;charset=utf8"});
          res.write(content.toString('ascii'));
          res.end();
      }
      switch (pathName) {
          case "/index":{
              showPage("./view/index.html", 200);
              break;
          }
          case "/about": {
              showPage("./view/about.html", 200);
              break;
          }
          default:{
              showPage("./view/404.html", 200);
              break;
          }
      }
  }
  let server = http.createServer(handler);
  server.listen(port, host);
  ```



## 1-12 全局系列

### 全局对象

***

> 浏览器中，window是全局对象；Node.js中，global是全局对象，所有全局对象都是global的属性。

### 全局对象与全局变量

***

+ 全局变量分类

  > 1. 在最外层定义的变量
  > 2. 全局对象的属性
  > 3. 隐式定义的变量

+ 注意

  > 1. Node.js中不可能在最外层定义变量，以为用户代码属于当前模块，模块本身不是最外层上下文
  > 2. 用let定义变量避免引入全局变量

+ 所有模块都可以调用

  > 1. global
  > 2. process：内置process模块，允许开发者与当前进程互动。
  > 3. console

+ 全局变量

  > 1. __filename
  >
  > 2. __dirname
  >
  > 3. setTimeout(cb,ms)
  >
  > 4. process
  >
  >    > 1. exit：`process.exit()` 方法以退出状态 `code` 指示 Node.js 同步地终止进程
  >    > 2. beforeExit：node清空事件循环，并且没有其他安排时触发这个事件！
  >    > 3. uncaughtException：当未捕获的 JavaScript 异常一直冒泡回到事件循环时，会触发 `'uncaughtException'` 事件
  >    > 4. Signal：进程收到信号时触发

+ 代码

  ```javascript
  console.log(__filename);
  console.log(__dirname)
  
  setTimeout(()=>{
      console.log("call setTimeout!");
  }, 3000);
  ```

  ```javascript
  process.on('exit', (code : number):void=>{
      console.log("退出码为:" + code);
  });
  
  console.log("程序执行结束!");
  ```

  

### 全局函数

***

> 1. setTimeout
> 2. clearTimeout
> 3. setInterval
> 4. clearInterval
> 5. require

### 准全局变量

***

> 1. module：当前模块
> 2. module.exports：当前模块对外输出接口，其它文件加载该模块，实际就是读取module.exports变量
> 3. module.id：模块的识别符
> 4. module.filename：模块文件名
> 5. module.loaded：模块是否完成加载
> 6. module.parent：返回使用该模块的模块
> 7. module.children：返回一个数组，表示模块用到的其它模块

**注意：用typescript的模块替代node.js的模块**



## 1-13 文件系统

### 异步和同步

***

```javascript
// 文件系统的所有API都有同步和异步的版本
import fs = require("fs");

// 异步读取
fs.readFile("../output.txt",(err: NodeJS.ErrnoException | null, data: Buffer):void=>{
    if (err){
        return console.error(err);
    }
    console.log("异步读取:" + data.toString());
});

//同步读取
let data : Buffer = fs.readFileSync("../output.txt");
console.log("同步读取:" + data.toString());

console.log("程序执行完毕!");
```

### 打开文件

***

+ 函数

  ```javascript
  fs.open(path, flags[,mode], callback)
  ```

+ 打开方式

  > + r：读取文件
  > + w：写入文件，文件不存在则创建
  > + a：追加模式

+ 示例

  ```javascript
  import fs = require("fs");
  
  // 异步打开
  console.log("准备打开文件!");
  
  fs.open('1.jss', "r", (err, fd)=>{
     if (err){
         return console.error(err);
     }
     console.log("文件打开成功!");
  });
  ```

### 获取文件信息

***

+ 函数

  ```javascript
  fs.stat(path, callback)
  ```

+ 文件属性stats类

  ```javascript
  // 是否为文件
  stats.isFile()
  
  // 是否为目录
  stats.isDirectory()
  
  // 是否为块设备
  stats.isBlockDevice()
  
  // 是否为字符设备
  stats.isCharacterDevice()
  
  // 是否为软连接
  stats.isSymbolicLink()
  
  // 是否为FIFO 管道
  stats.isFIFO()
  
  // 是否为Socket
  stats.isSocket()
  ```

+ 示例代码

  ```javascript
  import fs = require("fs");
  
  // 文件属性读取
  fs.stat('1.js',(err: NodeJS.ErrnoException | null, stats: fs.Stats):void=>{
      if (err){
          return console.error(err);
      }
      console.log(stats);
      console.log("读取文件信息成功!");
      console.log("是否为文件:" + stats.isFile());
      console.log("是否为目录:" + stats.isDirectory());
  });
  ```

  

### 写入文件

***

+ 函数

  ```javascript
  // file：文件描述符 或者文件名
  // data：可以是String或者Buffer
  // options：{encoding, mode, flag}
  // callback：写入失败时回调函数
  fs.writeFile(file, data[,options],callback)
  ```

+ 示例代码

  ```javascript
  import fs = require("fs");
  
  console.log("准备写入文件!");
  
  fs.writeFile("hello.txt", '我是写入的内容,我骄傲!',(err):void=>{
      if (err){
          return console.error(err);
      }
      console.log("内容写入成功!");
  
      console.log("读取写入的内容:");
      fs.readFile('hello.txt', (err, data):void=>{
          if (err){
              return console.error(err);
          }
          console.log("异步读取:" + data.toString());
      })
  });
  ```

### 读取文件

***

+ 函数

  ```c++
  // fd : 文件描述符
  // buffer：缓冲区
  // offset：缓冲区偏移量
  // length：要从文件中读取的字节数
  // position：文件读取的起始位置
  // callback：回调函数
  fs.read(fd, buffer, offset, length, position, callback)
  ```

+ 示例代码

  ```javascript
  import fs = require("fs");
  
  let buf : Buffer = Buffer.alloc(1024);
  fs.open("hello.txt", "r", (err : NodeJS.ErrnoException | null, fd : number) : void=>{
      if (err){
          return console.error(err);
      }
      console.log("文件打开成功!");
      console.log("准备读取文件:");
  
      fs.read(fd, buf, 0, buf.length, 0,(err:NodeJS.ErrnoException | null, bytesRead: number, buffer: Buffer):void=>{
          if (err){
              return console.error(err);
          }
          console.log(bytesRead + " 字节被读取!");
          if (bytesRead > 0){
              console.log(buf.slice(0,bytesRead).toString())
          }
      })
  });
  ```

### 关闭文件

***

+ 函数

  ```javascript
  fs.close(fd, callback)
  ```

+ 示例代码

  ```javascript
  import fs = require("fs");
  
  let buf : Buffer = Buffer.alloc(1024);
  
  fs.open('hello.txt', "r", (err, fd):void=>{
      if (err){
          return console.error(err);
      }
      console.log("文件打开成功!");
      console.log("准备读取文件:");
  
      fs.read(fd, buf, 0, buf.length, 0,(err, bytesReaded):void=>{
          if (err){
              return console.error(err);
          }
          if (bytesReaded > 0){
              console.log(buf.slice(0, bytesReaded).toString());
          }
  		// 关闭文件
          fs.close(fd,(err):void=>{
              if (err){
                  return console.error(err);
              }
              console.log("文件关闭成功!");
          })
      })
  })
  ```

### 截取文件 == TODO

***

+ 函数

  ```c++
  // fd : 文件描述符
  // len: 文件内容截取的长度
  // callback: 回调函数,没有参数
  fs.ftruncate(fd, len, callback)
  ```

  

### 删除文件

***

+ 函数

  ```c++
  // path:文件路径
  // callback:回调函数,没有参数
  fs.unlink(path, callback)
  ```

+ 示例

  ```javascript
  import fs = require("fs");
  
  console.log("准备删除文件:");
  fs.unlink('output.txt', (err ):void=>{
      if (err){
          return console.error(err);
      }
      console.log("文件删除成功!");
  })
  ```

### 创建目录

***

+ 函数

  ```javascript
  // path: 文件路径
  // mode: 设置目录权限,默认为0777
  // callback: 回调函数,没有参数
  fs.mkdir(path[,mode],callback)
  ```

+ 代码

  ```javascript
  import fs = require('fs');
  
  console.log("创建目录: ./view/tmp/");
  
  fs.mkdir("./view/temp/", (err):void=>{
      if (err){
          return console.error(err);
      }
      console.log("创建目录完毕!");
  })
  ```

### 读取目录

***

+ 函数

  ```javascript
  // path: 文件路径
  // callback: 回调函数,参数为err和files
  fs.readdir(path, callback)
  ```

+ 代码

  ```javascript
  import fs = require("fs");
  
  console.log("查看./view目录");
  
  fs.readdir('./view', (err: NodeJS.ErrnoException | null, files: string[]):void=>{
      if (err){
          return console.error(err);
      }
      files.forEach((file)=>{
          console.log(file);
      })
  });
  ```

  

### 删除目录

***

+ 函数

  ```javascript
  // path: 文件路径
  // callback: 回调函数,没有参数
  fs.rmdir(path, callback)
  ```

+ 示例

  ```javascript
  import fs = require("fs");
  console.log("删除./view/temp目录");
  fs.rmdir('./view/temp', (err):void=>{
      if (err){
          return console.error(err);
      }
      console.log("删除目录成功!");
  })
  ```

  

### 参考手册

***

[File System](https://nodejs.org/dist/latest-v12.x/docs/api/fs.html)

### 补充知识点

***

```javascript
// 附加写入文件
import fs = require("fs");

fs.open("1.js", "a",(err, fd):void=>{
    if (err){
        return console.error(err);
    }
    fs.writeFile(fd, "bb", (err):void=>{
        if (err){
            return console.error(err);
        }
        fs.close(fd,():void=>{
            console.log("关闭文件!");
        });
    })
})
```





## 1-14 GET-POST请求

### GET请求

***

```javascript
import http = require("http");
import url = require("url");
import util = require("util");
import {IncomingMessage, ServerResponse} from "http";


http.createServer((req: IncomingMessage, res: ServerResponse):void=>{
    res.writeHead(200,{'Content-Type':'text/plain;charset=utf-8'});
    res.end(util.inspect((url.parse(req.url as string, true))));
}).listen(3000);

// 请求url：http://127.0.0.1:3000/gm?name=xiaoming&age=90
// 浏览器打印结果：
Url {
  protocol: null,
  slashes: null,
  auth: null,
  host: null,
  port: null,
  hostname: null,
  hash: null,
  search: '?name=xiaoming&age=90',
  query: [Object: null prototype] { name: 'xiaoming', age: '90' },
  pathname: '/gm',
  path: '/gm?name=xiaoming&age=90',
  href: '/gm?name=xiaoming&age=90' }
```



### 获取URL参数

***

```javascript
// request:http://127.0.0.1:3000/gm?name=xiaoming&age=90
import http = require("http");
import url = require("url");
import util = require("util");
import {IncomingMessage, ServerResponse} from "http";


http.createServer((req: IncomingMessage, res: ServerResponse):void=>{
    let params = url.parse(req.url as string, true).query;

    res.writeHead(200, {'Content-Type':'text/plain;charset=UTF-8'});
    res.write("姓名:" + params.name);
    res.write('\n');
    res.write("年龄:" + params.age);
    res.end(); // 这个函数是什么意思?
}).listen(3000);
```

### 如何获取URL头部

****





### POST请求

***

```javascript
// node.js默认不会解析请求body
import http = require("http");
import querystring = require("querystring");
import  fs = require("fs");

let postHtml : string = "";
let buf : Buffer = Buffer.alloc(2048);
let fd = fs.openSync("./demo.html", 'r');
fs.readSync(fd,buf,0,buf.length,0);
fs.closeSync(fd);
postHtml = buf.toString();
http.createServer((req: http.IncomingMessage, res: http.ServerResponse):void=>{
    let body : string = "";
    req.on('data', (chunk : any):void=>{
        body += chunk;
    });

    req.on('end', ():void=>{
        let query : querystring.ParsedUrlQuery = querystring.parse(body);
        res.writeHead(200, {'Content-Type': 'text/html;charset=UTF-8'});
        if (query.name && query.age) {
            res.write("姓名:" + query.name);
            res.write("<br/>");
            res.write("年龄:" + query.age);
        }else{
            res.write(postHtml);
        }
        res.end();
    })
}).listen(3000);
```

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>post提交表单</title>
</head>
<body>

<form method="post">
    姓名: <input name = "name" /> <br/>
    职位: <input name = "age" /> <br/>
    <input type="submit">
</form>
</body>
</html>
```

