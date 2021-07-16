# 第一章 变量赋值

***

1. 简单赋值(:=)类似编程语言中的赋值方式

   ```makefile
   x := foo
   y := $(x)b
   x := new
    
   .PHONY : test
   test:
       @echo "y => $(y)"
       @echo "x => $(x)"
   ```

2. 递归赋值(=)影响到全部依赖于它的变量

   ```makefile
   x = foo
   y = $(x)b
   x = new
    
   .PHONY : test
   test:
       @echo "y => $(y)"
       @echo "x => $(x)"
   ```

   输出值:

   y = > newb

   x => new

3. 条件赋值(?=)变量未定义则赋值

   ```makefile
   x := foo
   y := $(x)b
   x ?= new
    
   .PHONY : test
   test:
       @echo "y => $(y)"
       @echo "x => $(x)"
   ```

   输出值:

   y => foob

   x = foo

4. 追加赋值(+=)

   ```makefile
   x := foo
   y := $(x)b
   x += $(y)
    
   .PHONY : test
   test:
       @echo "y => $(y)"
       @echo "x => $(x)"
   ```

   输出结果:

   y => foob

   x => foo foob



# 第二章 调用shell命令

***

1. 直接在makefile中用**$(shell ...)**

   ```makefile
   dir := $(shell pwd)
   test:
   	echo "dir => $(dir)"
   ```

2. 直接使用shell

   - shell命令必须在规则里面
   - 每行shell都是一个单独的进程。上一行定义的变量在下一行是无效的，因此要用**\\**拼接多行，类似C语言的宏函数
   - makefile调用shell时会对变量进行替换。makefile中定义的变量，用$(变量名)引用，如果是shell中的变量，用使用$$

   ```makefile
   # @指定不显示执行的命令
   all:
           @if [ "$(BUILD)" = "debug" ];then \
           echo "build debug"; \
           else \
           echo "build release"; \
           fi
           echo "done"
   ```

   下面的示例无法打印变量CC的值

   ```
   all:
           @CC="arm-linux-gcc"
           @echo $${CC}
   ```

   正确的用法

   ```makefile
   all:
           @CC="arm-linux-gcc";\
           echo $${CC}
   ```

   引用shell变量用$${变量名}，引用makefile变量用$(变量名)

   ```makefile
   SUBDIR := src example
   all:
           @for subdir in $(SUBDIR);\
           do \
           echo "building $${subdir}";\
           done
   ```



# 第三章 函数

***

+ wildcard：获取文件列表

  ```makefile
  # 获取工作目录下全部.tars文件列表
  $(wildcard *.tars)
  ```

+ patsubst：替换

  ```makefile
  # 首先使用“wildcard”函数获取工作目录下的.tars文件列表；之后将列表中所有文件名的后缀.tars替换为.h。这样我们就可以得到在当前目录可生成的.h文件列表
  $(patsubst %.tars,%.h, $(wildcard *.tars))
  ```

+ strip：去掉字符串开头的空格

+ filter：保留符号模式的字符串

  ```makefile
  # 保留 a.c b.c
  echo $(filter %.c,a.c b.c c.h e.tar)
  ```

+ filter-out：去掉符合模式的字符串

  ```makefile
  # 保留 c.t e.tar
  echo $(filter %.c,a.c b.c c.h e.tar)
  ```

+ sort：排序

  ```makefile
  # 返回bar foo lose
  echo $(sort foo bar lose)
  ```

+ dir：取目录，即最后一个反斜杠**之前**的部分，如果没有反斜杠，返回**./**

  ```makefile
  #打印 /home/wdz/ ./
  echo $(dir /home/wdz/a.txt b.txt)
  ```

+ notdir：取文件名，即最后一个反斜杠**之后**的部分

  ```makefile
  #打印 a.txt b.txt
  echo $(notdir /home/wdz/a.txt b.txt)
  ```

+ basename：取前缀，即扩展名前面的部分

  ```makefile
  #打印 /home/wdz/a b makefile
  echo $(basename /home/wdz/a.txt b.txt makefile)
  ```



# 第四章 特殊符号

***

+ $@：表示目标

+ $<：表示第一个依赖项

+ $^：表示全部依赖项

+ 通配符%：为每一个**.cpp**文件生成**.o**文件

  ```makefile
  %.o:%.cpp
  	g++ -c -o $@ $<
  ```

# 第五章 分支

***

+ ifneq：不等
+ ifeq：相等

# 第六章 其它

***

+ **include FILENAMES**

  如果*“**FILENAMES**”*列表中的任何一个文件不能正常读取而且不存在一个创建此文件的规则时*make*程序将会提示错误并退出。

+ **-include FILENAMES**

  当所包含的文件不存在或者不存在一个规则去创建它，*make*程序会继续执行，只有真正由于不能正确完成终极目标的重建时（某些必需的目标无法在当前已读取的*makefile*文件内容中找到正确的重建规则），才会提示致命错误并退出。



# 第七章 建议

***

使用Cmake来构建项目，更加简单易于维护


