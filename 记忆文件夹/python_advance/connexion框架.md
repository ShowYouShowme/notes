# 第一章 connexion框架使用说明

<font color=red>直接使用flask即可，不推荐使用这个框架，有坑</font>



## 1.1 安装框架

1. 安装框架

   ```shell
   pip install connexion
   ```

2. 安装ui

   ```shell
   pip install connexion[swagger-ui]
   ```



## 1.2 启动示例项目

1. hello.py

   ```python
   #!/usr/bin/env python3
   
   import connexion
   from flask import request
   
   
   def post_greeting(name: str) -> str:
       return 'Hello {name}'.format(name=name)
   
   if __name__ == '__main__':
       app = connexion.FlaskApp(__name__, port=9090, specification_dir='swagger/')
       app.add_api('helloworld-api.yaml', arguments={'title': 'Hello World Example'})
       app.run(debug=True)
   ```

2. swagger/helloworld-api.yaml：该文件对缩进有严格要求

   ```yaml
   swagger: "2.0"
   
   info:
     title: "{{title}}"
     version: "1.0"
   
   basePath: /v1.0
   
   paths:
     /greeting/{name}:
       post:
         summary: Generate greeting
         description: Generates a greeting message.
         operationId: hello.post_greeting
         produces:
           - text/plain;
         responses:
           200:
             description: greeting response
             schema:
               type: string
             examples:
               "text/plain": "Hello John"
         parameters:
           - name: name
             in: path
             description: Name of the person to greet.
             required: true
             type: string
   ```

3. 打开web-ui界面

   ```shell
   http://127.0.0.1:9090/v1.0/ui/
   ```

4. 查看完整路由

   ```python
   if __name__ == '__main__':
       app = connexion.FlaskApp(__name__, port=9090, specification_dir='swagger/')
       app.add_api('helloworld-api.yaml', arguments={'title': 'Hello World Example'})
       print(app.app.url_map) # 增加这一行
       app.run(debug=True)
   ```



## 1.3 yaml文件编写规范

1. [参考这里](https://editor.swagger.io/#/)

2. 说明

   + yaml里basePath 配置路由前缀
   + 默认ui的路由是：http://127.0.0.1:9090/v1.0/ui

3. 示例

   + get请求

     ```yaml
     # get请求,参数放在URL里面
       /query:
         get:
           summary: 查询身份证信息
           description: 通过身份证号码查出生日
           operationId: hello.query
           produces:
             - application/json
           responses:
             200:
               description: 出生年月日
               schema:
                 type: string
               examples:
                 "text/plain": "1990/08/08"
           parameters:
             - name: id
               in: query
               description: 身份证号码
               required: true
               type: string
     ```

   + post提交表单

     ```yaml
       /login:
         post:
           summary: 登录
           description: 客户端调用此接口来登录
           operationId: hello.login
           consumes:
             - application/x-www-form-urlencoded
           produces:
             - application/json
           responses:
             200:
               description: 出生年月日
               schema:
                 type: string
               examples:
                 "text/plain": "1990/08/08"
           parameters:
             - name: uname
               in: formData
               description: 帐号名
               "type": "string"
               required: true
             - name: upwd
               in: formData
               description: 密码
               "type": "string"
               required: true
     ```

   + POST请求，数据用json序列化

     ```yaml
       /sign_up:
         post:
           summary: 注册
           description: 注册帐号
           operationId: hello.sign_up
           consumes:
             - application/json
           produces:
             - application/json
           responses:
             200:
               description: 出生年月日
               schema:
                 type: string
               examples:
                 "text/plain": "1990/08/08"
           parameters:
             - name: data
               in: body
               required: true
               schema:
                 $ref: '#/definitions/User'
     
     definitions:
       User:
         type: object
         required:
           - uname
           - upwd
         properties:
           uname:
             type: string
             description: Unique identifier
             example: "123"
           upwd:
             type: string
             description: Pet's name
             example: "Susie"
             minLength: 1
             maxLength: 100
     ```

     