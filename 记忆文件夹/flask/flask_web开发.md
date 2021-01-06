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
  source venv/bin/active
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

