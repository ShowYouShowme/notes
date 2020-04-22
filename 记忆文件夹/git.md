# 常见问题

1. mac系统下git 终端显示中文乱码

   ```shell
   git config --global core.quotepath false
   ```



# 常用操作



## 1 检查状态

```shell
git status
```



## 2 克隆版库

```shell
git clone https://github.com/ShowYouShowme/notes.git
```



## 3 注册修改

```shell
git add ${file}
```



## 4 差异比较

```shell
git diff HEAD
```



## 5 提交

```shell
git add ${file}
git commit --message "增加data.txt文件"

# 或者
git commit -m "${comment}"
```



## 6 上载修改

+ 命令

  ```shell
  git push
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

  
## 7 获取数据

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

   



## 8 分支

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



## 9 commit

1. 丢弃提交

   + 彻底回到指定版本，丢弃代码中的修改

     ```shell
     git reset --hard ${commitID}
     ```

   + 只会退commit信息

     ```shell
     git reset --soft ${commitID}
     ```

     

## 10 日志

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





## 11 差异对比





## 12 储藏

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
```

