# 一、 常见命令



## 1.1 查看帮助信息

```
cmake --help
```





## 1.2 cmake-gui

windows上用cmake生成vs studio项目时，推荐用gui工具。

1. 设置源文件目录：where is the source code
2. 设置生成工程目录：where to build the binaries
3. 配置vs版本：点击Configure按钮
4. 生成工程：点击Generate按钮
5. 打开项目：点击Open Project 按钮



## 1.3 生成项目



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

   



# 第二章 编写CMake文件



## 2.1 例子

1. 基本项目

   ```cmake
   cmake_minimum_required(VERSION 3.10)
   
   # set the project name
   project(Tutorial)
   
   # add the executable
   add_executable(Tutorial example.c)
   
   # 增加动态链接库
   target_link_libraries(Tutorial PUBLIC pthread)
   
   # 第三方SDK 统一安装在/usr路径下,因此下面两个命令用不到
   ##############################################
   
   # 添加头文件目录
   # INCLUDE_DIRECTORIES
   
   # 添加库文件目录
   # LINK_DIRECTORIES
   ```



## 2.2 常用命令

 1. set

    ```
    设置变量的值。用unset()取消变量的值
    
    set(<variable> <value>... [PARENT_SCOPE])
    ```

 2. add_subdirectory

    ```shell
    将子目录添加到编译系统中，调用后cmake会自动进入该目录搜索CMakeLists.txt并进行编译
    
    add_subdirectory(source_dir [binary_dir] [EXCLUDE_FROM_ALL])
    ```

 3. aux_source_directory

    ```shell
    查找目录下的所有源文件，并保存到一个变量中。如果所有的源文件都在同一目录下且数量较多，那么使用这一命令会省去一个一个添加源文件的麻烦
    
    aux_source_directory(<dir> <variable>)
    ```

 4. INCLUDE_DIRECTORIES

    ```shell
    添加头文件目录
    ```

 5. LINK_DIRECTORIES

    ```shell
    添加库文件目录
    ```

 6. target_link_libraries

    ```shell
    添加动态库
    target_link_libraries(Tutorial PUBLIC pthread)
    ```