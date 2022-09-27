## 创建项目

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
   ```



## 调试项目

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
   >    添加debug配置，然后设置启动的js文件，最后断点启动项目即可
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



## 第三方包安装

### redis安装

***

1. 普通redis

   1. 安装redis包

      ```shell
      npm install redis --save
      ```

   2. 安装声明文件

      ```shell
      npm install @types/redis
      ```

2. ioredis：可以直接await操作

   1. 安装ioredis

      ```shell
      npm install ioredis
      ```

   2. 安装声明文件

      ```shell
      npm install @types/ioredis
      ```

      

### MySQL安装

***

1. 普通MySQL

   1. 安装MySQL包

      ```shell
      npm install mysql --save
      ```

   2. 安装MySQL声明文件

      ```shell
      npm install @types/mysql
      ```

2. typeorm

   1. 安装orm

      ```shell
      npm install typeorm 
      ```

3. sequelize

   1. 安装sequelize

      ```shell
      npm install sequelize
      ```

      


### typescript安装

***

```shell
npm install typescript -g
```

### 安装node声明文件

***

```shell
npm install @types/node
```

## npm教程

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
   >    ```shell
   >    # 安装模块后，模块的名称将加入到dependencies（生产阶段的依赖）
   >    npm install gulp --save 或 npm install gulp –S
   >    
   >    # package.json内容
   >    "dependencies": {
   >        "gulp": "^3.9.1"
   >    }
   >    ```
   >
   > 2. --save-dev 或者-D
   >
   >    ```shell
   >    # 安装模块后，模块名称将加入到devDependencies（开发阶段的依赖）
   >    npm install gulp --save-dev 或 npm install gulp –D
   >    
   >    # package.json 的devDependencies属性：
   >    "devDependencies": {
   >    
   >        "gulp": "^3.9.1"
   >    
   >    }
   >    ```
   >
   > 3. --save-optional 或者-O
   >
   >    ```shell
   >    # 安装模块后，模块名称将加入到optionalDependencies（可选阶段的依赖）
   >    npm install gulp --save-optional 或 npm install gulp -O
   >    
   >    # package.json 文件的optionalDependencies属性：
   >    "optionalDependencies": {
   >    
   >        "gulp": "^3.9.1"
   >    
   >           }
   >    ```
   >
   > 4. --save-exact 或者 -E 
   >
   >    ```shell
   >    # 精确安装指定模块版本
   >    npm install gulp-concat --save-exact 或 npm install gulp-concat –E
   >                            
   >    # package.json文件里"dependencies"属性的
   >                            
   >    "dependencies": {
   >                            
   >        "gulp-concat": "2.6.1"   //注意此处：版本号没有 ^
   >                            
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







# 使用Protobuf



## 安装pbjs

```ini
; https://www.npmjs.com/package/pbjs
npm install pbjs
```



## 生成ts文件

```ini
pbjs wire-format.proto --ts wire-format.ts
```



## 示例代码

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





# 引入js的模块

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





处理JSON

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



# Interface的用法

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







# 导入模块的方式

1. js的方式

   ```javascript
   const child_process = require('child_process')
   ```

2. ts的方式

   ```javascript
   // 等价于 const exec = require('child_process')
   // child_process 里面必须有默认导出
   import exec from 'child_process';
   ```
   
   ```javascript
   // 直接导入模块中的符号
   import {PI, Sum} from "./utility"
   ```
   



# 导出模块

```javascript
//普通导出
// 需要 import {...} from './...' 导入
export class PlayerManager{
    
}
```

```javascript
// 默认导出
// 导入方式  import Raking from './rank';
export default class Raking{
    
}
```

