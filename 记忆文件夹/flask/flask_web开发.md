# 第一章 安装



## 1.1 虚拟环境

+ 定义：python解释器的私有副本，在该环境中安装私有包，不会影响系统中安装的全局python解释器
+ 作用
  + 避免安装的包以及python版本和系统的冲突
  + 不需要管理员权限

## 1.2 创建虚拟环境

```shell
# step-1

sudo apt-get install python3-venv

# step-2
python3 -m venv ${virtual-environment-name}

## 例子
python3 -m venv venv
```



## 1.3 使用虚拟环境

+ Linux系统

  ```shell
  source venv/bin/activate
  ```

+ Win

  ```shell
  venv\Scripts\activate
  ```

  

## 1.4 安装flask

```shell
# 安装flask
pip install flask

# 查看虚拟环境中安装了哪些包
pip freeze


# 验证flask是否正确安装

(venv)$ python
>>> import flask  # 没有错误提醒即可
```





# 第二章 应用的基本结构



## 2.1 初始化

```shell
from flask import Flask
app = Flask(__name__)
```





## 2.2 路由和视图函数

+ 路由：处理URL和函数之间关系的程序称为路由

+ 定义路由

  ```shell
  @app.route('/')
  def index():
      return '<h1>Hello World!</h1>'
  ```

  ```shell
  def index():
      return '<h1>Hello World!</h1>'
      
  app.add_url_rule('/', 'index', index)
  ```

+ 可变路由

  ```shell
  @app.route('/user/<name>')
  def user(name):
      return '<h1>Hello {}!</h1>'.format(name)
  ```

  

## 2.3 完整应用

```python
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>Hello World!</h1>'
```





## 2.4 启动服务

+ Linux

  ```shell
  # hello.py是脚本文件名
  (venv) $ export FLASK_APP=hello.py
  (venv) $ flask run
  ```

+ Win

  ```shell
  set FLASK_APP=hello.py
  flask run
  ```

+ 编程的方式启动（不推荐）

  ```shell
  if __name__= '__main__':
  	app.run()
  ```

  



## 2.5 调试模式

+ 优点

  ```shell
  1. 项目中的源文件变动时，自动重启服务
  
  2. 当应用抛出未处理的异常，堆栈信息会出现在浏览器中
  ```

+ 缺点

  ```shell
  客户端通过调试器能请求执行远程代码，攻击服务器
  ```
  
+ 启动方式
  
  ```shell
  (venv) $ export FLASK_APP=hello.py
  (venv) $ export FLASK_DEBUG=1
  (venv) $ flask run
  ```
  
  
  
  