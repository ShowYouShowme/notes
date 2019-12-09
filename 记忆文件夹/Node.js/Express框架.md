## 2-1 初识Express框架

> 精简的、灵活的Node.js Web程序框架，为构建单页、多页以及混合的Web程序提供了一系列健壮的功能特性。



## 2-2 简单使用Express

### 安装Express

***

+ 安装包

  ```shell
  npm install express --save
  # 处理JSON,Raw,Text和URL编码的数据
  npm install body-parser --save
  # 解析Cookie的工具
  npm install cookie-parser --save
  # 处理enctype="multipart/form-data"
  npm install multer --save
  ```

+ 安装提示文件

  ```shell
  npm install @types/express
  npm install @types/body-parser
  npm install @types/cookie-parser
  npm install @types/multer
  ```

+ 查看express版本号

  ```shell
  npm list express
  ```

### 简单实例

***

```javascript
import express = require("express");
import {AddressInfo} from "net";

let app = express();

app.get("/",(req, res):void=>{
    res.send("Hello World!");
});

let port : number = 8081;
let host : string = "0.0.0.0";
let server = app.listen(port, host, ():void=>{
    let addrInfo : AddressInfo =  server.address() as AddressInfo;
    let h = addrInfo.address;
    let p = addrInfo.port;

    console.log("success", h, p );
});
```

### 请求和响应讲解

***

+ 文档 [链接](http://www.expressjs.com.cn/4x/api.html)

+ 示例代码

  ```javascript
  import express = require("express");
  import {AddressInfo} from "net";
  
  let app = express();
  
  app.get("/",(req, res):void=>{
      console.log(req.baseUrl);
      console.log(req.hostname);
      console.log(req.originalUrl);
      console.log(req.params);
      res.json({"name":"wzc"});
  });
  
  let port : number = 8081;
  let host : string = "0.0.0.0";
  let server = app.listen(port, host, ():void=>{
      let addrInfo : AddressInfo =  server.address() as AddressInfo;
      let h = addrInfo.address;
      let p = addrInfo.port;
  
      console.log("success", h, p );
  });
  ```

### 路由功能

***

```javascript
import express = require("express");
import {AddressInfo} from "net";

let app = express();

app.get("/",(req, res):void=>{
    res.send("我是主页GET请求!");
});

app.post("/", (req, res):void=>{
    res.send("我是主页POST请求");
});

app.get("/user", (req, res):void=>{
    res.send("我是个人中心!");
});

app.get("/db*cd",(req, res):void=>{
    res.send("正则匹配!");
})

let port : number = 8081;
let host : string = "0.0.0.0";
let server = app.listen(port, host, ():void=>{
    let addrInfo : AddressInfo =  server.address() as AddressInfo;
    let h = addrInfo.address;
    let p = addrInfo.port;

    console.log("success", h, p );
});
```



### 静态文件

***

```javascript
// 请求：http://127.0.0.1:8081/about.html

import express = require("express");
import {AddressInfo} from "net";

let app = express();
app.use(express.static('view'));
let port : number = 8081;
let host : string = "0.0.0.0";
let server = app.listen(port, host, ():void=>{
    let addrInfo : AddressInfo =  server.address() as AddressInfo;
    let h = addrInfo.address;
    let p = addrInfo.port;

    console.log("success", h, p );
});
```



### GET、POST方法

***



### 文件上传

***



### cookie管理

***

