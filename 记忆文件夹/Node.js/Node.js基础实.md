# 第一章  前言

安装开发环境

```shell
sudo apt install nodejs npm
```

指定版本安装

```shell
wget https://nodejs.org/dist/v16.17.0/node-v16.17.0-linux-x64.tar.xz
tar -xf node-v16.17.0-linux-x64.tar.xz
mv node-v16.17.0-linux-x64 ~/local/
#配置环境变量即可
```





## 1.1 创建项目

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
   "target": "es2016",
   ```

## 1.2 调试项目

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
## 1.3 代码跳转

***

> 部分符号，比如函数跳转不正常，先执行断点下来，再跳转即可！



## 1.4 第三方包安装

安装时，加上选项-E，精确版本

### 1.4.1 redis安装

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

### 1.4.2 MySQL安装

------

1. 普通MySQL

   ```shell
   npm install mysql --save
   
   # 安装声明文件
   npm install @types/mysql
   
   
   #可以使用Promise Promise.all await async 将回调改写为同步的模式
   ```

2. typeorm

   ```shell
   npm install typeorm 
   ```

3. sequelize

   ```shell
   npm install sequelize
   ```

### 1.4.3 typescript安装

------

```shell
npm install typescript -g
```



### 1.4.4 安装node声明文件

------

```shell
npm install @types/node
```



### 1.4.5 npm教程

1. 使用cnpm

   ```shell
   # 安装cnpm
   npm install cnpm -g --registry=https://registry.npm.taobao.org
   
   # 查看版本
   cnpm -v
   
   # 之后用cnpm命令替代npm
   ```

   

2. 切换阿里源

   ```shell
   npm config set registry https://registry.npm.taobao.org/
   
   # 查看切换是否成功
   npm config get registry
   ```

   

3. 配置代理

   ```shell
   #当安装包卡住，提示sill idealTree buildDeps的时候，设置代理即可
   npm config set proxy=http://127.0.0.1:8090
   ```

4. 查看包的版本信息

   ```shell
   #查看最新版本
   npm view gulp version 
   
   #查看全部版本
   npm view gulp versions
   ```

   

5. 全局安装

   ```shell
   npm install ${包名} -g
   ```

6. 安装

   ```shell
   #建议的安装方式,不改变大版本号和小版本号
   npm install protobufjs --save --save-prefix=~
   
   #默认的安装方式
   npm install ${包名}
   
   # 安装指定版本的包
   npm install ${包名}@${version}
   # 例子
   npm install  gulp@3.9.1
   
   # 安装package.json里面的全部依赖
   npm install
   ```

7. 执行`package.json`里面的指令

   ```shell
   npm run ${cmd}
   
   # 例子
   "scripts": {
       "start": "cross-env NODE_ENV=development webpack-dev-server --config webpack.dev.config.js",
       "build": "cross-env NODE_ENV=production webpack --config webpack.prod.config.js"
     },
   npm run start
   npm run build
   
   #完整的package.json的配置
   {
     "name": "interface_demo",
     "version": "1.0.0",
     "description": "",
     "main": "index.js",
     "scripts": {
       "build": "tsc",
       "start": "node .\\bin\\index.js",
       "test": "echo \"Error: no test specified\" && exit 1"
     },
     "keywords": [],
     "author": "",
     "license": "ISC"
   }
   
   ```

   

8. 卸载

   ```shell
   npm uninstall ${包名}
   ```

9. 更新

   ```shell
   npm update ${包名}
   ```

10. 检查包是否过时

   ```shell
   npm outdated
   ```

11. 列出安装的全部包

   ```shell
   npm ls
   ```

11. 参数说明

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



### 1.4.6 示例代码

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



### 1.4.7 版本前缀

1. 版本格式：X.Y.Z

   ```
   大版本号.次要版本号.小版本
   ```

2. version

   ```shell
   必须匹配某个版本
   
   如: 2.2.1, 表示必须依赖2.2.1版的依赖包
   ```

3. **\>version**

   ```
   必须大于某个版本
   
   如: >2.2.1, 表示必须依赖大于 >2.2.1版的依赖包
   ```

4. \>=version

   ```
   必须大于或等于某个版本
   
   如: >=2.2.1, 表示必须依赖大于或等于 >=2.2.1版的依赖包
   ```

5. \<version

   ```
   必须小于某个版本
   
   如: <2.2.1, 表示必须依赖小于 <2.2.1版的依赖包
   ```

6. **\<=version**

   ```
   必须小于或等于某个版本
   
   如: >=2.2.1, 表示必须依赖小于或等于 >=2.2.1版的依赖包
   ```

7. **\~version**

   ```
   不改变大版本号和次要版本号,小版本号随意
   
   注意:
   
   如果按照版本号格式,X.Y.Z,那么小版本号就是随意
   如: ~2.2.1, 表示 >=2.2.1 <2.3.0 版的依赖包 (可以是2.2.1, 2.2.2, 2.2.3, …, 2.2.n)
   如果版本号格式,X.Y,那么跟正规格式的意义相同
   如果版本号格式,X,那么次要版本号和小版本号可以随意
   如: ~2, 表示 >=2.0.0 < 3.0.0版的依赖包 (可以是2.0.0, 2.0.n, 2.1.0, …, 2.n.n)
   ```

8. **^version**

   ```
   版本号最左边非 0 数字的右侧可以任意
   
   如: ^2.2.1,表示 >=2.2.1 < 3.0.0版依赖包
   
   ^0.2.1,表示 >=0.2.1 <0.3.0版依赖包
   
   ^0.0,表示 >=0.0.0 <0.1.0版依赖包
   ```

9. **version号位置出现 X**

   ```
   X 的位置表示任意版本
   
   如: 2.2.x,表示 >=2.2.0 <2.3.0版依赖包
   ```

10. **version使用 \* 代替**

    ```
    任意版本, *""*也表示任意版本
    
    如: *, 表示 >=0.0.0版依赖包
    ```

11. **version(1) - version(2)**

    ```
    大于等于version(1),小于等于version(2)
    
    如: 2.2.1 - 2.3.1, 表示 >=2.2.1 <=2.3.1版依赖包
    ```

    





# 第二章 创建应用



## 2.1 node.js运行原理

php开发时，接受http请求并提供web页面由apache或nginx来处理，php仅处理业务。Node.js不仅处理业务，还实现了整个http服务器。



## 2.2 创建应用

***

```typescript
import http = require("http");

let server = http.createServer((req: http.IncomingMessage, res: http.ServerResponse) : void=>{
    res.writeHead(200,{'Content-Type':'text/plain'});
    res.end('Hello World!\n');
});

server.listen(8899,'0.0.0.0');
```



# 第三章 REPL



## 3.1 定义

***

Node.js的交互式解释器



## 3.2 简单示范

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



## 3.3 常用的REPL命令

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



# 第四章 回调函数



## 4.1 回调函数的机制原理

***

任务开始执行前注册回调函数，任务执行完毕执行回调函数！



## 4.2 简单范例

***

> 1. 阻塞代码
>
>    ```javascript
>    import fs = require("fs");
>    let fd : number = fs.openSync("configureNet.bat", "r");
>    let data : Buffer = Buffer.alloc(1024);
>    fs.readSync(fd, data, 0,1024,0);
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



# 第五章 事件循环



## 5.1 事件循环机制解释

***

基于观察者模式实现，有一个while事件主循环，类似Libevent，直到没有事件观察者就退出！



## 5.2 事件驱动程序

***

Node.js事件驱动模型中，有一个主循环监听事件，事件发生时触发回调函数。我们把它成为事件IO或非阻塞IO。



## 5.3 简单范例

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



## 5.4 Node应用程序如何工作

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





# 第六章 EventEmitter



## 6.1 EventEmitter类

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



## 6.2 EventEmitter常用方法

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



## 6.3 error事件

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



## 6.4 继承EventEmitter

1. 一般不会直接使用EventEmitter，而是在对象中继承
2. fs、net、http都是继承EventEmitter。





# 第七章 Stream

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

## 7.1 从流中读取数据

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



## 7.2 写入流

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



## 7.3 管道流

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



## 7.4 链式流

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





# 第八章 Buffer

+ 定义：存放二进制数据的缓冲区，类似一个整数数组



## 8.1 创建Buffer类

***

```javascript
let b1 : Buffer = new Buffer(10);
let b2 : Buffer = new Buffer([10, 20, 30, 40, 50]);
let b3 : Buffer = new Buffer("www.runoob.com", "utf-8");
```



## 8.2 写入缓冲区

***

```javascript
let buf : Buffer = new Buffer(10);
let len : number = buf.write("hello World!");
console.log("写入字节数:" + len);
```



## 8.3 从缓冲区读取数据

***

```javascript
let buf : Buffer = new Buffer(26);
for (let i : number = 0; i < 26; ++i){
    buf[i] = i + 97;
}
console.log(buf.toString('ascii'));
console.log(buf.toString('ascii', 0, 4));
```



## 8.4 将Buffer转换为JSON对象

***

```javascript
let buf : Buffer = new Buffer("i am BatMan");
let json : object = buf.toJSON();
console.log(json);
```



## 8.5 缓冲区合并

```javascript
let buf1 : Buffer = new Buffer("我的职业是");
let buf2 : Buffer = new Buffer("科学家");


let buf3 : Buffer = Buffer.concat([buf1, buf2]);

console.log("合并后的buf是:" + buf3.toString());
```



## 8.6 缓冲区比较

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



## 8.7 缓冲区裁剪

```javascript
let buf = new Buffer("ABCDEFHIJK");

let buf2 = buf.slice(1,3);

console.log(buf2.toString());
```



## 8.8 拷贝缓冲区

```javascript
// 与旧缓冲区指向同一块内存,只是索引不同
let buf = new Buffer("ABC");
let buf2 = new Buffer(3);
buf.copy(buf2);
console.log(buf2.toString());
```



## 8.9 缓冲区长度

```javascript
let buf : Buffer = new Buffer("1234567890");

console.log(buf.length)
```



## 8.10 方法参考手册

[Buffer文档](http://nodejs.cn/api/buffer.html)





# 第九章 模块系统

+ 定义：模块就是Node.JS代码文件

## 9.1 创建模块

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



## 9.2 服务端模块

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





# 第十章 函数



## 10.1 创建函数

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



## 10.2 匿名函数

***

```javascript
function nodeFun(fun : (param : string)=>void, value : string) {
    fun(value);
}

nodeFun((param : string) : void =>{
    console.log("param:" + param);
}, "Hello second Function!")
```



## 10.3 函数传递的工作原理

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



# 第十一章 路由

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



# 第十二章 全局系列

## 12.1 全局对象

***

> 浏览器中，window是全局对象；Node.js中，global是全局对象，所有全局对象都是global的属性。



## 12.2 全局对象与全局变量

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

  

## 12.3 全局函数

***

> 1. setTimeout
> 2. clearTimeout
> 3. setInterval
> 4. clearInterval
> 5. require



## 12.4 准全局变量

***

> 1. module：当前模块
> 2. module.exports：当前模块对外输出接口，其它文件加载该模块，实际就是读取module.exports变量
> 3. module.id：模块的识别符
> 4. module.filename：模块文件名
> 5. module.loaded：模块是否完成加载
> 6. module.parent：返回使用该模块的模块
> 7. module.children：返回一个数组，表示模块用到的其它模块

**注意：用typescript的模块替代node.js的模块**



# 第十三章 文件系统



## 13.1 异步和同步

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



## 13.2 打开文件

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

## 13.3 获取文件信息

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

  

## 13.4 写入文件

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

## 13.5 读取文件

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

## 13.6 关闭文件

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

## 13.7 截取文件 == TODO

***

+ 函数

  ```c++
  // fd : 文件描述符
  // len: 文件内容截取的长度
  // callback: 回调函数,没有参数
  fs.ftruncate(fd, len, callback)
  ```

  

## 13.8 删除文件

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

## 13.9 创建目录

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

## 13.10 读取目录

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

  

## 13.11 删除目录

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

  

## 13.12 参考手册

***

[File System](https://nodejs.org/dist/latest-v12.x/docs/api/fs.html)



## 13.13 补充知识点

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





# 第十四章 GET-POST请求



## 14.1 GET请求

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



## 14.2 获取URL参数

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

## 14.3 如何获取URL头部

****





## 14.4 POST请求

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



# 第十五章 promise

1. 函数体内部出现`await`关键词时，要在function前加`async`

2. 函数返回值为`Promise`时，调用该函数时加上`await`；在`Promise`里面使用resolve或者reject传出参数

3. resolve 和reject 后面的代码还能执行，如果不希望它们执行直接在resolve或者reject后面return

4. promise 在new的时候就开始执行了

5. promise([...]).then(res =>{}) 里面的res的结果次序和传入的promise一致

6. 示例代码

   ```javascript
   //利用promise + await 将回调改为顺序执行
   async function httpGet(){
       let [err,response, body] = await new Promise(function(resolve, reject){
           request({
               url: "http://127.0.0.1:8000/person.json",
               method: "GET",
           },function(err , response : any,body : any){
               resolve([err, response, body])
           })
       }) as [any,any,string] ;
       console.log(`err : ${err}`);
       console.log(`response : ${response}`);
       console.log(`body:${body}`);
   
       return body;
   }
   
   async function t1() {
       let val = await httpGet();
       console.log('val = ',val);
   }
   t1();
   ```

   ```javascript
   //等待多个任务执行完成
   async function check() {
       let v = await testPromise();
       console.log('v = ',v);
   
       let p1 = new Promise(function(resolve, reject){
           setTimeout(()=>{
               console.log('promise 1 finished');
               resolve(128);
           },3000)
       })
   
       let p2 = new Promise(function(resolve, reject){
           setTimeout(()=>{
               console.log('promise 2 finished');
               throw new Error('fuck you!')
               reject(329);
           },7000)
       })
   
       Promise.all([p1,p2]).then(res =>{
           console.log('res : ', res);
       }, reason =>{
           console.log(`捕获异常:${reason}`);
       })
   }
   ```

   ```javascript
   //await 与分支
   async function testReturn(params:number) {
       let val = params % 2;
       if(val == 0){
           let v2 = await new Promise(function(resolve, reject){
               setTimeout(function(){
                   resolve(120);
               },3000)
           }) as number;
           val = val + v2;
       }else{
           val += 50;
       }
       val += 12;
       return val;
   }
   
   async function getBranchRes(params:number) {
       let v = await testReturn(params);
       console.log('v = ',v);
   }
   
   getBranchRes(2);
   ```

   ```javascript
   // promise 和 await 一起使用
   async function test(){
     let p1 = new Promise((resolve, reject)=>{
       setTimeout(() => {
         console.log('p1 finished...');
         resolve(1);
       }, 5000);
     })
   
     let p2 = new Promise((resolve, reject)=>{
       setTimeout(() => {
         console.log('p22 finished...');
         resolve(2);
       }, 2000);
     })
   
   
     let result = await Promise.all([p1,p2]);
     console.log(`result : ${result}`);
   };
   ```

   





# 第十六章 Protobuf



## 16.1 google实现的protobuf



### 16.1.1 安装依赖

```ini
npm install google-protobuf
```



### 16.1.2 安装protoc

```ini
; 21.5的版本不能生成js的文件
wget https://github.com/protocolbuffers/protobuf/releases/download/v3.20.1/protoc-3.20.1-win64.zip
```



### 16.1.3 生成文件

```ini
protoc --js_out=import_style=commonjs,binary:. cmd_net.proto
```



### 16.1.4 示例代码

```javascript
//webstorm里面是不能代码补全的
const WebSocket = require('ws');
const cmd_net = require('./cmd_net_pb')
const {json} = require("stream/consumers");

let p1 = new cmd_net.TPackage()
p1.setMaincmd(cmd_net.MainCmdID.SYS)
p1.setSubcmd(cmd_net.SubCmdID.SYS_HEART_ASK)

const client = new WebSocket('ws://localhost:8080')
client.on('open', function (){
    client.send(p1.serializeBinary())  //序列化
})

client.on('close', function (){
    console.log('peer close the connect!')
})

client.on('message', function (data){
    let message = cmd_net.TPackage.deserializeBinary(data)  //反序列化
    let mainCmd = message.getMaincmd()
    let subCmd = message.getSubcmd()
    console.log(JSON.stringify(message.toObject()))   //message打印为JSON
})

setInterval(function (){
    console.log('....')
}, 1500)
```





## 16.2 protobufjs

完全用js实现的protobuf。



### 16.2.1 安装

```ini
[安装包]
cmd = npm install protobufjs --save --save-prefix=~
url = https://www.npmjs.com/package/protobufjs

[安装命令行]
cmd = npm install protobufjs-cli --save --save-prefix=~
url = https://www.npmjs.com/package/protobufjs-cli

[生成js和ts文件]
cmd-1 = ./node_modules/protobufjs-cli/bin/pbjs -t static-module -w commonjs -o compiled.js msg.proto
cmd-2 = ./node_modules/protobufjs-cli/bin/pbts -o compiled.d.ts compiled.js
```



## 16.2.2 示例代码



1. proto

   ```protobuf
   syntax = "proto3";
   
   package ns;
   
   message Login {
       string name = 1;
       string pwd = 2;
   }
   message Address{
       string province = 1;
       string city = 2;
       string country = 3;
   }
   ```

2. 代码

   ```typescript
   import {ns} from './compiled'
   let message : ns.ILogin = {};
   message.name = 'nash';
   message.pwd  = '123456';
   let msg : ns.Login = ns.Login.create(message);
   let buffer = ns.Login.encode(msg).finish();
   var decodedMessage = ns.Login.decode(buffer);
   console.log(`decode data : ${JSON.stringify(decodedMessage.toJSON())}`);
   ```

   



# 第十七章 异常处理

1. nodejs没有main函数，因此无法try...catch整个main函数来捕获全部异常

2. 捕获全部异常的方法

   ```javascript
   process.on('uncaughtException',function (err){
       console.log("有一个未捕获的异常",err) // ws是否还能正常监听呢
   })
   ```

3. 回调函数里面的异常不能在外面捕获

4. try...catch await 函数，只能捕获reject，不能捕获promise的异常。

5. 可以throw 各种类型，比如bool，string等等

   ```javascript
   throw "Error2";   // String type
   throw 42;         // Number type
   throw true;       // Boolean type
   throw {toString: function() { return "I'm an object!"; } };
   ```

6. 判断特定类型的异常

   ```javascript
   try {
     myRoutine();
   } catch (e) {
     if (e instanceof RangeError) {
       // statements to handle this very common expected error
     } else {
       throw e;  // re-throw the error unchanged
     }
   }
   ```

7. 抛出基本错误

   ```javascript
   try {
     throw new Error('Whoops!')
   } catch (e) {
     console.error(e.name + ': ' + e.message)
   }
   ```

   





# 第十八章 HTTP客户端



## 18.1 安装

```shell
#website:https://github.com/request/request
npm install request
```



## 18.2 GET请求

```javascript
request({
    url: "http://192.168.2.110:8100",
    method: "GET",
},function(err : any, response : any,body : any){
    if(err){
        console.log(err);
        return;
    }
    console.log(response);
    console.log(body);
})
```



## 18.3 POST请求

```javascript
const request = require('request')
request({
    url: "http://192.168.2.110:9002/server/login/checklogintoken",
    method : "POST",
    json : true,
    headers:{
        "content-type": "application/json"
    },
    body:{
        "token" : "65bad951c31b8777d512d832bcc633d718a1411f"
    }
},function(err : any, response : any, body:any){
    if(err){
        console.log(err);
        return;
    }
    console.log(response);
    console.log(body);
})
```





# 第十九章  技巧



## 19.1 对象合并

```javascript
let obj = {
    name : "nash",
    age  : 128
};


let person = {
    uid : 99,
    ...obj
}

console.log(person)


let hello = 'justin';
let age = 25;

let obj = {
  'salary' : 1290,
  hello,
  age
};
```







# 第二十章 日志



## 20.1 安装

```shell
npm install log4js
```





## 20.2 用法



### 20.2.1 打印日志到控制台

```javascript
import log4js from "log4js";

const logger = log4js.getLogger();
logger.level = "debug";
logger.debug("Some debug messages");
```



### 20.2.2 打印日志到文件

```javascript
const log4js = require("log4js");
log4js.configure({
  appenders: { cheeseLogs: { type: "file", filename: "cheese.log" },
               console: { type: 'console' }},
  categories: { default: { appenders: ["cheeseLogs","console"], level: "error" } },
});

const logger = log4js.getLogger();
logger.trace("Entering cheese testing");
logger.debug("Got cheese.");
logger.info("Cheese is Comté.");
logger.warn("Cheese is quite smelly.");
logger.error("Cheese is too ripe!");
logger.fatal("Cheese was breeding ground for listeria.");
```





### 20.2.3 按日期滚动

```javascript
import * as log4js from 'log4js';
log4js.configure({
    appenders: { cheese: { type: "dateFile", filename: "cheese", pattern:'yyyy-MM-dd.log', alwaysIncludePattern: true,} },
    categories: { default: { appenders: ["cheese"], level: "error" } },
})

let logger = log4js.getLogger();
logger.trace("this is trace");
logger.debug('this is debug');
logger.info('this is info');
logger.warn('this is warn');
logger.error('this is error[]');
logger.fatal('this is fatal');
console.log(".......")
```



## 20.2.4 配置vscode debug时显示

```shell
#在launch.json 里面增加
"outputCapture": "std"
```





# 第二十一章 websocket



## 21.1 安装

```shell
npm install --save ws
npm install @types/ws
```





## 21.2 使用

注意：ws触发close事件后，会自动close文件描述符，不需要在代码里写ws.close()。浏览器最小化后，里面的ws链接会失去网络，类似拔了网线，测试需要把浏览器一直放前台运行，最好获取鼠标的焦点。





# 第二十二章 类型断言



## 22.1 内置数据类型

```javascript
typeof "John"                // 返回 string
typeof 3.14                  // 返回 number
typeof false                 // 返回 boolean
typeof [1,2,3,4]             // 返回 object
typeof {name:'John', age:34} // 返回 object
typeof null                  // 返回 object
typeof undefined             // 返回 undefined
```



## 22.2 值类型和引用类型

```ini
[值类型]
v1 = string
v2 = number
v3 = boolean

[引用类型]
v1 = Object
v2 = array
v3 = Map
v3 = Set
```







# 第二十三章  执行shell



```javascript
var exec = require('child_process').exec;
 
exec('ls -al', function(error, stdout, stderr){
    if(error) {
        console.error('error: ' + error);
        return;
    }
    console.log('stdout: ' + stdout);
    console.log('stderr: ' + typeof stderr);
})
```





# 第二十四章  登录鉴权



## 24.1 使用JWT

```javascript
//token具有过期时间,任何client得到这个token都可以发起请求
import express = require('express');
import bodyParser = require("body-parser");
import jwt from 'jsonwebtoken';
const port = 3001;
const app = express();
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))


let secretKey : string = 'Nh+xUwT@VYv9F_yT';

app.post('/login', (req, res) => {
    let token = jwt.sign({username : 'wxs'}, secretKey, {expiresIn : '100s'});
    res.json({
        code : 0,
        msg : '登录成功',
        token
    })
});

app.get('/getUserInfo', (req, res)=>{
    try {
        let query = req.query as any;
        let info = jwt.verify(query.token, secretKey) as any;
        console.log('info : ', info['username']);
        res.send('一个get请求想获取用户信息');
    } catch (error) {
        res.send('过期了,请重新登录!');
    }
})



app.listen(port, '0.0.0.0', () => {
    console.log(`Example app listening on port ${port}`);
});
```





## 24.2 使用session

原理：客户端登录时，服务器产生一个session对象，存到map里面；key是cookie，将它返回给客户端。客户端下次请求时头部加上Cookie即可，任何http客户端只要带上这个头部都可以访问。其实和token差不多，建议用jwt替换！



```javascript
//install: npm install express-session

import express = require('express');
import bodyParser = require("body-parser");
var session = require('express-session')
const port = 3001;
const app = express();
app.use(bodyParser.json())
app.use(bodyParser.urlencoded({ extended: true }))

app.use(session({ secret: 'keyboard cat', cookie: { maxAge: 60000 }}))

// Access the session as req.session
app.get('/', function(req, res, next) {
  let session  = (req as any).session;
  if (session.views) {
    session.views++
    res.setHeader('Content-Type', 'text/html')
    res.write('<p>views: ' + session.views + '</p>')
    res.write('<p>expires in: ' + (session.cookie.maxAge / 1000) + 's</p>')
    res.end()
  } else {
    session.views = 1
    res.end('welcome to the session demo. refresh!')
  }
})

app.listen(port, '0.0.0.0', () => {
    console.log(`Example app listening on port ${port}`);
});
```







# 第二十五章 EXCEL

将excel转化为json是游戏开发常见的一个需求。



1. 安装依赖

   ```shell
   npm install excel
   ```

2. 代码

   ```javascript
   // 增加声明
   // declare module 'excel';
   
   import parseXlsx from 'excel';
    
   parseXlsx('excel_mac_2011-basic.xlsx').then((data : any) => {
     console.log(`data: ${data}` );
   
     let result = [];
     let fields = data[0];
     for(let i = 1; i < (data as Array<any>).length; ++i){
       let item = {} as any;
       for(let j = 0; j < fields.length; ++j){
         let key   = fields[j] as string;
         let value =  data[i][j];
         item[key] = value;
         result.push(item);
       }
     }
   
     console.log(JSON.stringify(result));
   });
   ```




# 第十六章 时间和日期



## 16.1 获取时间戳

```javascript
//毫秒时间戳
let ts = new Date().getTime()
```



## 16.2 打印时间

```javascript
let datetime = (new Date()).toLocaleString();
console.log(datetime);
```





# 第十七章 调度系统

类似于cron的调度系统，常用的开源组件有xxl-job和node-schedule。



网址：https://github.com/node-schedule/node-schedule



## 17.1 安装

```shell
npm install node-schedule
```





# 第十八章 进程



## 18.1 环境变量



### 18.1.1 配置

```ini
[配置文件]
path = ~/.bashrc

[配置环境变量]
export PHP_ADDR="192.168.2.102:9103"
```





### 18.1.2 获取环境变量

```javascript
console.log(JSON.stringify(process.env));

let php_addr = process.env.PHP_ADDR;
console.log(php_addr);

let php_port = process.env.PHP_PORT;
console.log(php_port);
if(php_port == undefined){
        console.log("变量不存在!");
}
```





# 第十九章 进程管理工具



## 19.1 systemd

具体内容参考Linux实战技能，实际部署时需要root权限，比较麻烦！



## 19.2 pm2

官方网站：https://pm2.keymetrics.io/docs/usage/quick-start/



### 19.2.1 安装

```shell
npm install pm2 -g
```



### 19.2.2 启动服务

```shell
pm2 start bin/index.js --name schedule

#开发阶段
pm2 start bin/index.js --name schedule --no-autorestart
```



启动参数

- `--watch`：监听应用目录的变化，一旦发生变化，自动重启。如果要精确监听、不见听的目录，最好通过配置文件。
- `-i --instances`：启用多少个实例，可用于负载均衡。如果`-i 0`或者`-i max`，则根据当前机器核数确定实例数目。
- `--ignore-watch`：排除监听的目录/文件，可以是特定的文件名，也可以是正则。比如`--ignore-watch="test node_modules "some scripts""`
- `-n --name`：应用的名称。查看应用信息的时候可以用到。
- `-o --output <path>`：标准输出日志文件的路径。
- `-e --error <path>`：错误输出日志文件的路径。
- `--interpreter <interpreter>`：the interpreter pm2 should use for executing app (bash, python...)。比如你用的coffee script来编写应用。
- --no-autorestart：不自动重启，开发阶段最好加上，可以及时排查错误





### 19.2.3 查看日志

```shell
pm2 logs schedule --raw
```



### 19.2.4 查看进程状态

```shell
pm2 list
```





### 19.2.5 监控进程

```shell
pm2 monit schedule
```



### 19.2.6 停止

```ini
[停止特定应用]
cmd = pm2 stop app_name|app_id

[停止全部应用]
cmd = pm2 stop all
```



### 19.2.7 重启

```shell
pm2 restart app_name|app_id
```



### 19.2.8 删除

```shell
pm2 delete app_name|app_id
```





### 19.2.9 开机启动

1. 生成开机启动 pm2 服务的配置文件

   ```shell
   pm2 startup
   #把输入的命令粘贴到终端运行
   ```

2. 保存当前 pm2 运行的各个应用

   ```shell
   pm2 save
   ```

   



### 19.2.10 查看服务的元数据

```shell
pm2 show ${srv_name}
```



### 19.1.11 产生配置文件

```ini
cmd = pm2 init 或者 pm2 ecosystem
```

