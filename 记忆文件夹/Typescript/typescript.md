## 创建项目

1. 初始化npm包管理器

   ```shell
   npm init
   ```

2. 创建项目配置文件

   ```shell
   tsc --init
   ```

3. 修改项目配置

   ```shell
   "sourceMap": true,
   "outDir": "./bin",
   "allowJs": true,
   "target": "es6",
   ```





## 第三方包安装

### redis安装

***

1. 安装redis包

   ```shell
   npm install redis --save
   ```

2. 安装声明文件

   ```shell
   npm install @types/redis
   ```




### MySQL安装

***

1. 安装MySQL包

   ```shell
   npm install mysql --save
   ```

2. 安装MySQL声明文件

   ```shell
   npm install @types/mysql
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



