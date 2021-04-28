# 一、 常见命令



## 1.1 查看帮助信息

```
cmake --help
```





## 1.2 生成项目



### 常见生成选项

***

```shell
  Visual Studio 15 2017 [arch] = Generates Visual Studio 2017 project files.
                                 Optional [arch] can be "Win64" or "ARM".
  Visual Studio 14 2015 [arch] = Generates Visual Studio 2015 project files.
                                 Optional [arch] can be "Win64" or "ARM".
  Visual Studio 12 2013 [arch] = Generates Visual Studio 2013 project files.
                                 Optional [arch] can be "Win64" or "ARM".
  Visual Studio 11 2012 [arch] = Generates Visual Studio 2012 project files.
                                 Optional [arch] can be "Win64" or "ARM".
  Visual Studio 10 2010 [arch] = Generates Visual Studio 2010 project files.
                                 Optional [arch] can be "Win64" or "IA64".
  Visual Studio 9 2008 [arch]  = Generates Visual Studio 2008 project files.
                                 Optional [arch] can be "Win64" or "IA64".
  Borland Makefiles            = Generates Borland makefiles.
  NMake Makefiles              = Generates NMake makefiles.
  Unix Makefiles               = Generates standard UNIX makefiles.
```

### 常见生成命令

***

1. 生成vs项目

   ```shell
   ## 第一步 生成项目
   # 生成vs2017 32位项目
   cmake -G "Visual Studio 15 2017" ../../../source
   
   # 生成vs2017 64位项目
   cmake -G "Visual Studio 15 2017 Win64" ../../../source
   
   ## 第二步 编译 打开 *.sln 解决方案
   用VS打开项目，点击生成-->生成解决方案 即可
   
   ## 第三步 安装[必须用管理员身份运行VS,因为文件安装在C盘]
   生成INSTALL项目
   ```

   

2. 生成UNIX makefile

   ```shell
   cmake -G "Unix Makefiles" ../../../source
   ```

3. 生成NMAKE makefile

   ```shell
   # 用管理员身份运行VS的工具命令提示[安装需要管理员权限]
   
   cmake -G "NMake Makefiles" ../../../source
   
   nmake
   
   nmake install
   ```

   