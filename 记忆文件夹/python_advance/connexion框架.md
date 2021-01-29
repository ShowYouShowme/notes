# 第一章 connexion框架使用说明



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

   