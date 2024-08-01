# 第一章 创建项目

1. 初始化npm包管理器

   ```shell
   npm init
   ```

2. 创建项目配置文件

   ```shell
   #如果失败，先安装typescript：npm install -g typescript
   tsc --init
   ```

3. 修改项目配置

   ```shell
   "sourceMap": true,
   "outDir": "./bin",
   "allowJs": true,
   "target": "es2016",
   //true:严格空值检查模式，此模式下null和undefined无法赋值给其他类型的变量,比如自定义类,为了开发方便可以设置为false
   "strictNullChecks": true,
   ```



# 第二章 调试项目

1. 编译生成javascript代码

   ```shell
   tsc
   ```

2. 断点调试

   > 1. webstorm：推荐使用
   >
   >    在ts代码里面打断点，然后启动bin目录下生成的js文件即可
   >
   >    ```shell
   >    0.按照上面修改tsconfig.json的四个配置
   >    1.点击run
   >    2.点击Edit configurations
   >    3.设置JavaScript file:bin\index.js
   >    4.在ts里面打断点:比如在index.ts里面打断点就能调试了
   >    ```
   >
   > 
   >
   > 2. vscode
   >
   >    添加debug配置，然后设置启动的js文件，最后断点启动项目即可；默认情况下DEBUG CONSOLE 无法输入，需要加入配置项"console": "integratedTerminal"
   >
   >    ```shell
   >    #TODO 也可以点击运行和调试,然后创建调试文件
   >    #1. 项目根目录创建文件夹.vscode
   >    #2. 创建调试配置文件launch.json
   >    #3. 配置文件写入如下内容
   >    {
   >        // 使用 IntelliSense 了解相关属性。 
   >        // 悬停以查看现有属性的描述。
   >        // 欲了解更多信息，请访问: https://go.microsoft.com/fwlink/?linkid=830387
   >        "version": "0.2.0",
   >        "configurations": [
   >            {
   >                "type": "node",
   >                "request": "launch",
   >                "name": "Launch Program",
   >                "skipFiles": [
   >                    "<node_internals>/**"
   >                ],
   >                "program": "${workspaceFolder}\\index.ts",
   >                "outFiles": [
   >                    "${workspaceFolder}/**/*.js"
   >                ]
   >            }
   >        ]
   >    }
   >    ```
   >
   > 



## 示例代码

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







# 第三章 使用Protobuf



## 3.1 安装pbjs

```ini
; https://www.npmjs.com/package/pbjs
; 推荐使用proto2 ,因为 proto3 如果int32 等类型不传值,客户端解析能得到0; proto2 可以判断是否为undefined
; pbjs的实现和官方proto有点差异,即使proto3,如果不传值,依然可以读取到undefined
; 如果客户端也是js/ts开发，建议用pbjs
npm install pbjs

[常用数据类型]
;枚举
T1 = enum
;整数, int64需要结合Long.js来使用
;发送int64给客户端时,先用Long.fromNumber()构造 Long，再发送出去;
;收到客户端的int64时,先用Long.fromValue() 将int64转换为Long,然后再用Long.toNumber()将Long转换为nodejs的number类型
T2 = int32/int64
;字符串
T3 = string
;二进制数组
T4 = bytes
;数组,map也用数组表示
T5 = repeated 

; 浮点数几乎用不到,浮点数有三种表示方式 1: string  2： 整数(带单位) 3: float/double
; 浮点数在运算过程中会导致精度丢失
```



## 3.2 生成ts文件

```ini
pbjs wire-format.proto --ts wire-format.ts
```



## 3.3 示例代码

```typescript
import * as proto from "./cmd_net"

let message : proto.TPackage = {}
message.MainCmd = proto.MainCmdID.ACCOUNTS
message.SubCmd  = proto.SubCmdID.ACCOUNTS_TOKEN_LOGON_REQ

let req : proto.CTokenLogonReq = {}
req.GameID = 124
req.Token = "65bad951c31b8777d512d832bcc633d718a1411f"
message.Data = proto.encodeCTokenLogonReq(req)
let buf = proto.encodeTPackage(message)

let m2 : proto.TPackage = {}
m2 = proto.decodeTPackage(buf)
console.log(JSON.stringify(m2))
let r2 = proto.decodeCTokenLogonReq(m2.Data as Uint8Array)
console.log(JSON.stringify(r2))
console.log("......")
```



int64的处理

```javascript
import * as proto from "./cmd_net"
import Long from "long";

//PB 的声明
// message TTest{
//     int64 money = 1;
//     int64 gold = 2;
// }


//构造Long类型的数字
let v1 : Long = Long.fromNumber(1234567);
let v2 : Long = Long.fromString('123456789123456');
console.log(`v1 = ${v1}, v2 = ${v2}`);

//构造pb的int64,然后发送给client
let t1 : proto.TTest = {};
t1.money = Long.fromString('1289');


//将客户端发的int64转换为Long
let t2 :  proto.TTest = {}
t2.gold = {
    low: 100,
    high: 200,
    unsigned: false,
}
let v4 : Long = Long.fromValue(t2.gold);
console.log(`v4 = ${v4}`);


let v5 : Long = Long.fromString('858993459300');
console.log(`v5 = ${v5}`);
```





# 第四章 引入js的模块

模块代码utility.js

```javascript
const PI = 3.14

function Sum(a, b){
    return a + b
}

function Person(name){
    this.name = name
    this.say = ()=>{
        console.log("I'm " + this.name)
    }
}

module.exports = {
    PI,
    Sum,
    Person
}
```





## 方法一

```javascript
//引入自己写的模块
import {PI, Sum} from "./utility"

console.log(PI)

let a : number = 1
let b : number = 20
let c : number = Sum(a,b)
console.log("a + b = ", c)
console.log("...")
```





## 方法二

```javascript
//需要先安装依赖:npm i --save-dev @types/node
//引入自己写的模块
const Helper = require("./utility") // 注意和方法一的区别

//或者   效果和上面的一样
//import  Helper = require("./utility")
console.log(Helper.PI)

let a : number = 12
let b : number = 208
let c : number = Helper.Sum(a,b) // 调用方式和方法一不一样
console.log("a + b = ", c)
console.log("...")
```



真实代码

```javascript
//npm install ws --save
//引入nodejs或者npm install安装的模块
const WS = require("ws"); //引入nodejs的模块


const client = new WS.WebSocket('ws://127.0.0.1:8080');
client.on('open', ()=>{
    console.log("链接建立成功!");
});
client.on('message', (data:any)=>{
    console.log("data : ", String(data))
    console.log("...")
});
client.on('close', ()=>{
    console.log("connection closed")
});

console.log("....")
```





# 第五章 JSON

```javascript
//一般是发起http请求时用
interface IPerson{
    name ?: string;
    age  ?: number;
}

let s2 : string = '{\"name\":\"powell\",\"age\":28,\"address\":\"/home/url/page.html\"}'
let p : IPerson = JSON.parse(s2)
console.log(p.name + " " + p.age)
console.log("successful")
```



# 第五章 Interface

```typescript
interface IPerson{
    name ?: string;
    age  ?: number;
}

let p : IPerson = {}
p.age = 1290;
p.name = "trump";
console.log(JSON.stringify(p))
console.log("successful")
```







# 第六章 模块



## 6.1 导入

1. 导入js模块

   ```javascript
   const child_process = require('child_process')
   ```

2. 导入ts模块

   ```javascript
   // 等价于 const exec = require('child_process')
   // child_process 里面必须有默认导出
   import exec from 'child_process';
   ```
   
   ```javascript
   // 直接导入模块中的符号
   import {PI, Sum} from "./utility"
   ```
   



## 6.2 导出

1. 普通导出

   ```javascript
   // 导入 import {...} from './...'
   export class PlayerManager{}
   ```

   

2. 默认导出

   ```javascript
   // 导入  import Raking from './rank';
   export default class Raking{}
   ```







# 第七章 声明文件

1. 声明文件可以提供代码补全的功能

2. 项目根目录下创建main.d.ts(相同目录下不能存在文件main.js 或者main.ts)

3. 编写声明

   ```javascript
   //声明js模块,可以使用import导入
   declare module 'excel';
   
   //模块声明
   declare module 'cmd_pb'{
       export class requestModel{
           msg : string;
           code : string;
   
           toObject() : any;
   
           serializeBinary() : any;
   
           getMsg(): string;
   
           setMsg(param : string) : void;
   
           getCode() : string;
   
           setCode(param : string) : void;
       }
   }
   
   
   //声明函数
   declare function giveMeMoney(str: string): void;
   
   //声明变量
   declare var ant:string
   
   
   
   //声明命名空间
   declare namespace space {
   
       function func(str: string): string;
     
       let num: number;
     
     }
   ```




# 第八章 es6特性



## 8.1 多返回值

```typescript
function calculateAllScore(cardArr: CardInfo[]): [number, boolean] {
    return [score, canDeclare]
}

let [tScore, tCanDeclare] = calculateAllScore(tRetArr);
```



## 8.2 切片

```typescript
let arr : number[] = {11,22,33,44,55}

// arr[1:3)
let arr2 = arr.slice(1,3) 
```



## 8.3 解构

```typescript
let [a, b, c] = [1, 2, 3]; // 基本
let { a, b } = { a: 'aaa', b: 'bbb' }; // 对象模型的解构 前后两个kay需对应
```



## 8.4 构造对象

```typescript
let name : string = "tylor"
let age : number = 19

let info  = {
    name,
    age
}
```



## 8.5 Spread / Rest 操作符

```typescript
// Spread
var s = ['1', '2', '3'];
function f(s1,s2,s3){
    console.log(`Hello ${s1},${s2},${s3}`); //ES6新增字符串中加入变量和表达式
}
f(...s); //Hello 1,2,3

// 利用Spread 复制数组
let aa = [11,22,33]
let bb = [...aa]



// Rest
function myBio(firstName, lastName, ...otherInfo) { 
  return otherInfo;
}

// Invoke myBio function while passing five arguments to its parameters:
myBio("Oluwatobi", "Sofela", "CodeSweetly", "Web Developer", "Male");

// The invocation above will return:
["CodeSweetly", "Web Developer", "Male"]
```



## 8.6 模板字面值

```typescript
const name = "ExplainThis";
// 不用樣板字面值（Template Literals）
console.log("Hello " + name + "!");
// 使用樣板字面值（Template Literals）
console.log(`Hello ${name}!`);
```



## 8.7 箭头函数

```typescript
() => expression

param => expression

(param) => expression

(param1, paramN) => expression

() => {
  statements
}

param => {
  statements
}

(param1, paramN) => {
  statements
}

```



## 8.8 let 与 const

定义变量的方式。



## 8.9 map类型

1. 使用es6的map

   ```typescript
   const map1 = new Map();
   
   map1.set('a', 1);
   map1.set('b', 2);
   map1.set('c', 3);
   
   console.log(map1.get('a'));
   // Expected output: 1
   
   map1.set('a', 97);
   
   console.log(map1.get('a'));
   // Expected output: 97
   
   console.log(map1.size);
   // Expected output: 3
   
   map1.delete('b');
   
   console.log(map1.size);
   // Expected output: 2
   
   
   // 遍历
   for (const [key, value] of myMap) {
     console.log(`${key} = ${value}`);
   }
   // 0 = zero
   // 1 = one
   
   for (const key of myMap.keys()) {
     console.log(key);
   }
   // 0
   // 1
   
   for (const value of myMap.values()) {
     console.log(value);
   }
   ```

2. 使用对象自己定义， 自定义类型无法使用for(let elem of arr)遍历

   ```typescript
   // 索引签名
   let cardMap: { [key: number]: number } = {}
   ```
   
3. Record：Record 是把索引签名进行了封装

   ```typescript
   let m1 : Record<number, number> = {}
   ```

   方法2和3表示的map只能使用for(let key in obj)遍历，而且key是string类型。因此可能需要将key转换为特定类型，比如number。

   



## 8.10 循环

```typescript
for(let i = 0; i < arr.length; i++)
    
    
arr.forEach()    

// 遍历Array、Map、Set
for (let item of arr)
    
// 用于遍历对象属性    
for (let i in arr)    
```





# 第九章 常见问题

vscode的powershell无法执行tsc

1. 管理员身份运行 window.powershell
2. 执行：get-ExecutionPolicy，显示Restricted，表示状态是禁止的;
3. 执行：set-ExecutionPolicy
4. 会提示输入参数：RemoteSigned
5. 会提示进行 选择： Y





配置vscode 启动前编译

1. 配置编译的task.json文件

   ```json
   {
       "version": "2.0.0",
       "tasks": [
           {
               "label": "compile",
               "type": "shell",
               "command": "tsc"
           }
       ]
   }
   ```

   

2. 在launch.json里面配置preLaunchTask

   ```json
   {
       "version": "0.2.0",
       "configurations": [
           {
               "type": "node",
               "request": "launch",
               "name": "Launch Program",
               "skipFiles": [
                   "<node_internals>/**"
               ],
               // 该字段值为对应task的lable
               "preLaunchTask": "compile",
               "program": "${workspaceFolder}\\bin\\main.js",
               "outFiles": [
                   "${workspaceFolder}/**/*.js"
               ]
           }
       ]
   }
   ```

   

