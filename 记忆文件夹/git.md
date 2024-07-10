#  第一章 常见问题

1. mac系统下git 终端显示中文乱码

   ```shell
   git config --global core.quotepath false
   ```

2. 安装目录

   ```shell
   Win下安装于默认目录，否则可能会有bug，比如代码无法push到GitHub
   ```

3. 使用GitHub开源项目二次开发时，遵守以下原则

   + 不要使用release版本，要直接git clone 代码
   + 不要使用master分支，要手动切换到指定tag

4. git-server 安装

   ```shell
   wget -O gitea https://dl.gitea.io/gitea/1.16.9/gitea-1.16.9-linux-amd64
   chmod +x gitea
   
   ./gitea web
   # 第一次运行会显示管理员账号和密码
   
   # 数据库选择sqlite3
   
   # 地址配置为ip 而不是localhost
   
   # 修改密码, 工作目录和启动时保持一致
   ./gitea admin user change-password --username roglic --password mm123456
   ```
   
   



# 第二章 常用操作

***

## 2.1 检查状态

```shell
git status
```



## 2.2 克隆版库

```shell
git clone https://github.com/ShowYouShowme/notes.git


# 打印日志
GIT_TRACE=2 git clone https://github.com/cloudwu/skynet.git
```



## 2.3 注册修改

***

1. 添加单个文件

   ```shell
   # 用小乌龟commit时,要先在文件前打勾,这就是打勾对应的命令行
   git add ${file}
   ```

   

2. 添加多个文件

   ```shell
   git add ${file1} ${file2} ${file3}
   ```

3. 添加指定目录下的文件

   ```shell
   git config/* 	#config以及config下所有文件
   
   git home/*.php 	#home目录下所有的php文件
   ```

4. 添加所有文件

   ```shell
   git add .
   
   git add --all
   ```

5. 取消注册

   ```shell
   git reset
   ```

   



## 2.4 差异比较

```shell
# 对比所有文件
git diff HEAD

# 对比单个文件
git diff app.py

# 简写
git diff
```



## 2.5 提交

```shell
git add ${file}
git commit --message "增加data.txt文件"

# 或者
git commit -m "${comment}"
```



## 2.6 上载修改

+ 命令

  ```shell
  git push
  
  
  # 连tags 一起推送
  git push --tags
  ```

+ 上载失败

  ```shell
  # step1
  git pull
  
  # step2
  解决冲突 使用git diff 查看冲突的地方
  
  # step3
  git add ${files}
  
  # step4 
  git commit --message "${comment}"
  
  # step5
  git push
  ```

  
## 2.7 获取数据

1. 只获取数据

   ```shell
   # 命令
   git fetch
   
   
   # 查看远程分支
   git branch -r
   
   # 查看本地分支
   git branch
   ```

2. 获取数据+合并

   ```shell
   # 命令
   git pull
   
   # 可能会失败，提示"error: Your local changes to the following files would be overwritten by merge:"
   # 失败原因:其它开发者的提交中修改了文件a，而你本地的文件a也被修改了
   
   # 解决方案
   
   # step1 => 暂存本地修改
   git stash
   
   # step2 => 获取数据
   git pull
   
   # step3 => 恢复本地修改
   git stash pop  # 查看 git stash list
   
   # step4 => 处理冲突 使用git diff 查看冲突的内容
   
   ```

3. pull 的问题

   + 详情：There is no tracking information for the current branch

   + 解决方案

     1. 指定远程分支

        ```shell
        # 指定把远程master 分支抓下来
        git pull origin master
        ```

     2. 和远程分支关联

        ```shell
        git branch --set-upstream-to=origin/master master
        git pull
        ```

        



## 2.8 分支

1. 合并分支

   ```shell
   # 将feature分支合并到当前分支
   git merge feature
   
   
   # 问题 => 合并分支出错
   # 原因 => 本地修改了文件A,其它分支正好对文件A有修改
   # 解决方案
   # step1 => 暂存本地修改
   git stash
   
   # step2 => 合并分支
   git merge target_branch
   
   # step3 => 恢复暂存区的数据
   git stash pop
   
   # step4 => 处理冲突 用git diff 查看处理
   
   ```

2. 切换分支

   ```shell
   git checkout target-branch
   ```

3. 创建分支

   + 在当前提交上创建分支

     ```shell
     git branch a-branch
     ```

   + 在现有分支上创建

     ```shell
     git branch b-branch older-branch
     ```

4. 删除分支

   + 删除其它分支

     ```shell
     git branch -d b-branch
     ```

   + 删除当前所在分支

     ```shell
     git branch -D b-branch
     ```

5. 查看分支

   + 查看本地分支

     ```shell
     git branch
     ```

     

   + 查看远程分支

     ```shell
     git branch -r
     ```

     

   + 查看全部分支

     ```shell
     git branch -a
     ```

6. 切换远程分支[非master，比如develop]

   ```shell
   # checkout远程remotes/origin/develop,在本地重命名为develop,并切换到develop
   git checkout -b develop remotes/origin/develop
   ```

7. 重命名分支

   + 重命名本地分支

     ```ini
     [重命名当前分支]
     cmd = git branch -m new_branch_name
     
     [重命名其它分支]
     cmd = git branch -m old_branch_name new_branch_name
     ```

   + 重命名远程分支

     ```ini
     ;重命名本地分支
     step-1 = git branch -m new_branch_name
     
     ;删除远程分支
     step-2 = git push --delete origin old_branch_name
     
     ;上传新命名的本地分支
     step-3 = git push origin new_branch_name
     
     ;本地分支和远程分支关联
     step-4 = git branch --set-upstream-to origin/new_branch_name
     
     
     [附录]
     ;查看本地分支和远程分支的关联情况
     cmd = git branch -vv
     ```

   

8. 推送本地新分支到仓库

   ```ini
   ;仓库没有该分支,推送时会报错
   ;fatal: The current branch dev-branka has no upstream branch
   
   CMD = git push --set-upstream origin ${localBranchName}
   EXAMPLE = git push --set-upstream origin dev-branka
   ```

9. 配置分支保护，某些分支仅允许指定的人员push，最常见的是release和dev分支，只有项目管理员能push

   ```ini
   ;使用的服务是gitea
   
   cmd = 项目 --> 分支 --> 分支保护 -->启动分支保护 --> 受白名单限制的推送(选择指定用户即可)
   ```

10. 开发时的使用

    ```ini
    开发分支 = dev
    
    测试    = 打tag并加上beta后缀,比如 v3.0.0-beta
    
    生产    = v3.0.0
    ```

    

   

   

   

   



## 2.9 commit

1. 丢弃提交

   + 彻底回到指定版本，丢弃代码中的修改

     ```shell
     git reset --hard ${commitID}
     ```

   + 只会退commit信息

     ```shell
     git reset --soft ${commitID}
     ```

   + 执行[commit](https://so.csdn.net/so/search?q=commit&spm=1001.2101.3001.7020)后，还没执行push时，想撤销这次的commit
   
     ```shell
     # 不删除工作空间的改动代码 ，撤销commit，不撤销git add file [常用]
     git reset --soft HEAD^
     
     # 删除工作空间的改动代码，撤销commit且撤销add  [慎用]
     git reset --hard HEAD^
     ```
   
     

## 2.10 日志

```shell
# 命令一
git log

# 只显示注释
git log --oneline

# 限制输出条目
git log -${num}

# 查看远程分支的日志
git log origin/master
```



## 2.11 储藏

```shell
# 储藏修改
git stash

# 恢复修改

## method1
git stash pop

## method2
git stash pop stash@{1}


# 查看储藏区内容
git stash list

# 储藏部分文件
git stash -p # 根据提示输入，"y"表示储藏，"n"表示不储藏
```





## 2.12 丢弃文件修改

***

```shell
# 类似svn的revert
git checkout -- main.cpp
```



## 2.13 创建版本库

***

+ 创建裸版本库

  ```shell
  git init --bare
  ```

+ 创建普通版本库

  ```shell
  git init
  ```




## 2.14 变基

***

```ini
        dev
   dev-li     dev-lj
   
;如果dev-li先合并分支,等dev-lj开发完成后,先rebase,再合并分支
```





## 2.15 tag

1. 查看tag

   ```SHELL
   # 查看全部tag
   git tag -l -n
   
   # 查看特定tag的详细信息
   git show v2.1.2
   ```

2. 打tag

   ```SHELL
   # 在指定commit上打tag
   git tag test_tag c809ddbf83939a89659e51dc2a5fe183af384233
   
   # 在最前面的commit上打tag
   git tag -a v2.1.2 -m "Version 2.1.2"
   ```

3. 删除tag

   ```SHELL
   git tag -d test_tag
   ```

4. 推送tag

   ```shell
   git push --tags
   ```

5. 切换到tag

   ```shell
   git checkout ${tagName}
   ```

   



## 2.16 子模块

```shell
# 初始化本地配置文件
git submodule init

# 检出父仓库列出的commit
git submodule update
```



## 2.17 忽略不想提交的文件

***

1. 项目根目录创建文件`.gitignore`

2. 编辑配置文件内容

   ```shell
   node_modules/
   package.json
   package-lock.json
   views/
   .idea/
   ether.js
   go.mod
   go.sum
   init.sql
   ```




## 2.18 文件重命名

```shell
git mv readme README.md
```



# 第三章 管理

***



## 3.1 git配置代理

1. 使用命令

   ```shell
   #全局代理
   #http代理：
   git config --global http.proxy http://127.0.0.1:8090
   git config --global https.proxy https://127.0.0.1:8090
   
   # 只有github使用代理
   git config --global http.https://github.com.proxy http://127.0.0.1:8090
   git config --global https.https://github.com.proxy https://127.0.0.1:8090
   ```
   
2. 编辑文件

   ```shell
   #在文件 ~/.gitconfig 添加：
   [http]
   proxy = http://127.0.0.1:8090
   [https]
   proxy = https://127.0.0.1:8090
   ```

3. 取消代理

   ```shell
   git config --global --unset http.proxy
   git config --global --unset https.proxy
   ```
   
4. 配置样例

   ```shell
   [credential]
           helper = store
   [user]
           email = wzc199088@gmail.com
           name = wzc 
   [http "https://github.com"]
           #proxy = http://127.0.0.1:8090
           proxy = socks5://127.0.0.1:8099
   [https "https://github.com"]
           #proxy = https://127.0.0.1:8090
           proxy = socks5://127.0.0.1:8099
   ```

   



## 3.2 保存账号密码

***

```shell
#在文件 ~/.gitconfig 添加：
[credential]                                                                    
    helper = store
    
    
# 或者 输入以下命令
git config --global credential.helper store
```



## 3.3 配置邮箱和用户名

```shell
git config --global user.email "wzc_0618@126.com"
git config --global user.name "wzc"
```



## 3.4 github配置

1. 配置access token
2. 使用用户名+ token(替代密码)登录
3. token 把 repo 权限勾上即可



# 第四章 多分支开发模式

***

1. 主分支用来分布生产版本，偶尔用来修复bug
2. develop分支用来开发
   + 如果有多个开发者，每个功能点，基于develop分支上再创建分支来开发，开发完成合并至develop
   + 如果单个开发者，直接在develop上面开发
   + 如果主分支有修复bug的提交，develop分支要rebase主分支
   + 发布版本时，把develop合并至master再发布





# 第五章 创建仓库



## 5.1 从命令行创建

```shell
touch README.md
git init
git checkout -b dev
git add README.md
git commit -m "first commit"
git remote add origin http://192.168.2.110:3000/roglic/protocol.git
git push -u origin dev
```





## 5.2 推送已创建仓库

```shell
git remote add origin http://192.168.2.110:3000/roglic/protocol.git
git push -u origin dev
```





# 第六章 安装



```shell
 sudo yum -y install expat-devel
 #下载源码
 wget https://github.com/git/git/archive/refs/tags/v2.39.1.tar.gz
 #解压
 tar -zxvf v2.39.1.tar.gz
 #进入目录
 cd git-2.39.1/
 #编译
 make prefix=$HOME/local/git -j8
 #安装
 make prefix=$HOME/local/git install -j8
 #配置环境变量
 export PATH=$PATH:$HOME/local/git/bin
```





# 常见问题处理

1. 虚拟机git访问github慢

   + 在win上开启letsvpn

   + 虚拟机采用nat网络，共用宿主机的网络

     

     

     
   
   

