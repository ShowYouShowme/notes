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

+ GET方法

  ```javascript
  import express = require("express");
  import {AddressInfo} from "net";
  
  let app = express();
  
  app.get("/", (req, res):void=>{
      res.sendFile(__dirname + "/" + "form.html");
  });
  app.get("/pro_get", (req, res):void=>{
      let response = {
          "name" : req.query.name,
          "age": req.query.age
      };
      res.end(JSON.stringify(response));
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

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>express表单提交get方法</title>
  </head>
  <body>
      <form action="http://127.0.0.1:8081/pro_get" method="get">
          name: <input type="text" name="name"> <br/>
          age:<input type="text" name="age"> <br/>
          <input type="submit" value="提交">
      </form>
  </body>
  </html>
  ```

+ POST方法

  ```javascript
  import express = require("express");
  import {AddressInfo} from "net";
  import bodyParser = require("body-parser");
  let urlencodeParser = bodyParser.urlencoded({extended:false})
  
  let app = express();
  
  
  app.get("/", (req, res):void=>{
      res.sendFile(__dirname + "/" + "form.html");
  });
  
  // 定义post方法的路由,配置解码器
  app.post("/pro_post", urlencodeParser,(req, res):void=>{
      let response = {
          "name" : req.body.name,
          "age": req.body.age
      };
      res.end(JSON.stringify(response));
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

  HTML

  ```html
  <!DOCTYPE html>
  <html lang="en">
  <head>
      <meta charset="UTF-8">
      <title>express表单提交post方法</title>
  </head>
  <body>
      <form action="http://127.0.0.1:8081/pro_post" method="post">
          name: <input type="text" name="name"> <br/>
          age:<input type="text" name="age"> <br/>
          <input type="submit" value="提交">
      </form>
  </body>
  </html>
  ```

  

### 文件上传

***

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>文件上传演示</title>
</head>
<body>
<h3>文件上传:</h3>
选择一个文件上传:<br/>
<form action="file_upload" method="post" enctype="multipart/form-data">
    <input type="file" name="image" size="50">
    <br/>
    <input type="submit" value="文件上传">
</form>
</body>
</html>
```

```javascript
import express = require("express");
import fs = require("fs");
import bodyParser = require("body-parser");
import multer = require("multer");



let app : express.Application = express();
app.use(express.static('public'));
app.use(bodyParser.urlencoded({extended : false}));
app.use(multer({dest:'/tmp'}).array('image'));

app.get("/", (req: express.Request, res : express.Response):void=>{
    res.sendFile(__dirname + "/" + "file_upload.html");
});

app.post('/file_upload', (req : express.Request, res : express.Response):void=>{
    let files   : Express.Multer.File[] = req.files as Express.Multer.File[];
    let file    : Express.Multer.File   = files[0];
    console.log(file);

    let des_file : string = __dirname + "/" + file.originalname;
    fs.readFile(file.path, (err, data):void=>{
        fs.writeFile(des_file, data, (err):void=>{
            let response : any = null;
            if (err){
                console.error(err);
            } else{
                response = {
                    message:'File uploaded successfully',
                    filename:file.originalname
                }
            }
            console.log(response);
            res.end(JSON.stringify(response));
        })
    })

});

let server = app.listen(8081);
```



### cookie管理

***

+ 定义

  > 访问一个页面时，服务器在下行的http报文中，命令浏览器存储一个字符串；当浏览器再访问同一个域的时候，将把这个字符串携带到上行的http请求当中。

+ 特点

  > 1. cookie保存在浏览器本地
  > 2. cookie不加密，用户可以正常看到
  > 3. 用户可以删除cookie或者禁用它
  > 4. cookie可以被篡改
  > 5. cookie可以用于攻击
  > 6. cookie存储量小，未来会被localStorage取代。

+ 使用

  > 1. 安装
  >
  >    ```shell
  >    npm install cookie-parser --save
  >    ```
  >
  > 2. 引入
  >
  >    ```javascript
  >    import cookieParser = require("cookie-parser");
  >    ```
  >
  > 3. 设置中间件
  >
  >    ```javascript
  >    app.use(cookieParser());
  >    ```
  >
  > 4. 设置cookie
  >
  >    ```javascript
  >    res.cookie("citys", citys, {maxAge:60*1000*10});
  >    ```
  >
  > 5. 获取cookie
  >
  >    ```javascript
  >    res.cookie("citys", citys, {maxAge:60*1000*10});
  >    ```

+ 相关属性

  > 1. domain：域名
  > 2. name=value：键值对，Expires：过期时间
  > 3. maxAge：最大失效时间，设置在多久之后失效
  > 4. secure：为true时，仅在https中有效
  > 5. Path：影响到的路径
  > 6. httpOnly：微软对COOKIE的拓展。设置了httpOnly属性后，通过程序(js脚本，applet等)无法读取COOKIE信息
  > 7. signed：是否签名cookie。true会对cookie签名，需要用res.signedCookies访问。被篡改签名的cookie会被服务器拒绝，并且cookie值重置。

+ 代码

  ```javascript
  import express = require("express");
  import cookieParser = require("cookie-parser");
  
  let app = express();
  app.use(cookieParser());
  
  app.get("/", (req : express.Request, res: express.Response):void=>{
     res.send(req.cookies.citys);
  });
  
  app.get("/lvyou", (req : express.Request, res : express.Response):void=>{
     let city : string    = req.query.city;
     let citys : string[]= req.cookies.citys;
     if (citys){
         citys.push(city);
     }else{
         citys = []
     }
  
     res.cookie("citys", citys, {maxAge:60*1000*10});
  
     res.send(city);
  });
  
  app.listen(8085);
  ```




### 中间件
***

+ bodyParser()

  支持 JSON, urlencoded和multipart requests的请求体解析中间件

  ```javascript
  app.use(express.bodyParser());
   
  // 等同于:
  app.use(express.json());
  app.use(express.urlencoded());
  app.use(express.multipart());
  ```

+ compress()

  通过gzip / deflate压缩响应数据. 这个中间件应该放置在所有的中间件最前面以保证所有的返回都是被压缩的

  ```javascript
  app.use(express.logger());
  app.use(express.compress());
  app.use(express.methodOverride());
  app.use(express.bodyParser());
  ```

+ cookieParser()

  解析请求头里的Cookie, 并用cookie名字的键值对形式放在 `req.cookies` 你也可以通过传递一个`secret` 字符串激活签名了的cookie

  ```javascript
  app.use(express.cookieParser());
  app.use(express.cookieParser('some secret'));
  ```

+ basicAuth

  基本的认证中间件，在req.user里添加用户名用户名和密码的例子

  ```javascript
  app.use(express.basicAuth('username', 'password'));
  ```

  