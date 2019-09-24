# 1 认识shell

## 1.1 什么是shell

+ shell是命令解释器

+ shell的种类

  ```
  cat /etc/shells
  ```

+ CentOS 7默认使用的shell是bash

## 1.2 Linux的启动过程

+ 启动过程

  1. BIOS
  2. MBR：决定是否可引导
  3. grub：选择内核
  4. kernel
  5. systemd：1号进程 
  6. 系统初始化
  7. shell

+ 启动过程涉及的文件

  1. MBR查看

     ```shell
     dd if=/dev/sda of=mbr2.bin bs=512 count=1
     hexdump -C mbr2.bin
     ```

  2. grub查看

     ```sh
     # 进入grub目录
     cd /boot/grub2
     # 查看默认引导的内核
     grub2-editenv list
     # 查看当前使用的内核
     uname -r
     ```

  3. 引导程序

     ```shell
     # CentOS 6
     which init
     cd /etc/rc.d/
     
     # CentOS 7
     cd /etc/systemd/system
     
     # 在下面的目录读取启动service
     cd /usr/lib/systemd/system
     ```

     

## 1.3 如何编写shell脚本

+ 编写步骤

  + 使用脚本文件保存需要执行的命令
  + 赋予该文件执行权限**chmod u+x filename**

+ 示例

  ```bash
  #!/bin/bash
  cd /var/
  ls
  pwd
  du -sh
  ```

  **第一行告诉系统使用bash来解释脚本**

+ 执行方式

  + bash 1.sh：用bash解释执行
  + ./1.sh：用系统默认解释器执行

## 1.4 shell脚本的执行方式

+ **bash ./1.sh ：子进程里运行**
+ ./1.sh：子进程运行
+ **source ./1.sh：当前终端运行**
+ . 1.sh：当前终端运行

## 1.5 内建命令和外部命令的区别

+ 内建命令不需要创建子进程
+ 内建命令对当前Shell生效





# 2 管道与重定向

## 2-1 管道与管道符

+ 作用：进程间通信

+ 示例1

  ```shell
  cat a.txt | more
  ```

+ 示例2

  ```shell
  cat | ps -f
  
  #查看进程状态
  cd /proc/${进程PID}/fd
  ls -l
  ```

  

## 2-2 子进程与子shell

管道符连接的命令都是创建子进程来执行的

## 2-3 重定向符号

+ 输入重定向：<

  ```
  read var < /path/to/a/file
  ```

+ 输出重定向：">"  ">>" "2>" "&>"

  + ">"：文件存在则先清空再输入
  + ">>"：附加
  + "2>"：错误重定向
  + "&>"：正确和错误信息全部重定向至指定文件

+ 示例

  1. 统计文件行数

     ```shell
     wc -l < /etc/passwd
     ```

  2. 获取变量值

     ```shell
     read var < a.txt
     ```

  3. 输出重定向

     ```shell
     # 注意下面两种方式的区别
     echo abc > a.txt
     echo def >> a.txt
     ```

  4. 错误重定向

     ```
     nocmd 2> c.txt
     ```

  5. 不管正确还是错误，全部重定向至指定文件

     ```
     nocmd &> c.txt
     ```

  6. 输入和输出重定向组合使用：用shell脚本生成配置文件[晦涩]

     ```shell
     #!/bin/bash
     
     cat > /root/a.sh <<EOF
     
     echo "hello bash"
     EOF
     
     ```



# 3 变量

## 3-1 变量的定义

+ 命名规则：包含数字、字母、下划线，不能以数字开头
+ Shell里面只有字符串一种变量类型

## 3-2 变量的赋值

+ 变量名=变量值

  ```shell
  # 等号左右不能有空格
  a=123
  ```

+ 使用let为变量赋值(不建议使用)

  ```
  let a=10+20
  ```

+ 将命令赋值给变量(不建议使用)

  ```
  cmd=ls
  ```

+ 将命令执行结果赋值给变量

  ```shell
  # 方式一
  result=$(ls -l /etc)
  
  # 方式二,不建议使用此方法，容易混淆
  result = `ls -l /etc`
  ```

  **注意：变量值有空格等特殊字符用""包含**

+ 案例

  ```
  cmd1=$(ls /root)
  
  str1="hello bash"
  
  str2="hello \"bash\""
  ```

  

## 3-3 变量的引用和作用范围

引用方式：

1. ${变量名}
2. $变量名



作用范围：

+ 默认作用范围：当前bash可以访问，子进程、平行进程和父进程均不可访问

  ```shell
  a=1
  # 进入子bash
  bash
  echo ${a} # 输出空白
  a=2
  exit
  echo ${a} # 输出1
  ```

  

+ 变量的导出：export，导出后子进程可以访问

+ 变量的删除：unset

## 3-5 系统的环境变量

+ 环境变量：每个Shell打开都可以获取的变量，可以认为是全局变量

  ```shell
  env | more
  
  echo ${USER}
  
  echo ${UID}
  
  echo ${PATH}
  
  # 添加搜索路径 对当前终端和子shell生效，对其它终端无效
  PATH=${PATH}:/root
  echo ${PATH}
  
  # 可以让终端提示增加时间、ip、完整路径等
  echo ${PS1}
  ```

+ set：可以查看环境变量、预定义变量和位置变量

  + 预定义变量

    ```shell
    # 上条命令执行正确返回0
    $?
    
    #  显示当前进程PID
    $$
    
    # 当前进程名称
    $0
    ```

  + 位置变量：获取用户传入的参数

    ```shell
    
    # ${1}:传入的第一个参数
    echo "param1:${1},param2:{$2}"
    
    # 小技巧(脑残)
    pos2=${2-_} # 有第二个参数时pos2值为传入的参数，否则为"_"
    ```

    

## 3-6 环境变量配置文件

**配置文件**

****

+ /etc/profile：所有用户通用
+ /etc/profile.d/
+ ~/.bash_profile：用户特有的配置
+ ~/.bashrc：用户特有的配置
+ /etc/bashrc：所有用户通用

**登录方式**

****

1. login shell

   ```shell
   su - root
   ```

   配置文件加载次序

   ```
   /etc/profile
   ~/.bash_profile
   ~/.bashrc
   /etc/bashrc
   ```

2. noLogin shell

   ```
   su root
   ```

   配置文件加载次序

   ```
   ~/.bashrc
   /etc/bashrc
   ```

   **不建议使用该模式**



**让配置文件立即生效**

****

1. 关掉终端，重新打开
2. source ${配置文件名}



**定义环境变量**

****

```shell
export PATH=${PATH}:/new/path
```



## 3-7 数组

+ 定义数组

  ```
  IPTS=( 10.0.0.1 10.0.0.2 10.0.0.3)
  ```

+ 显示数组的所有元素

  ```
  echo ${IPTS[@]}
  ```

+ 显示数组元素的个数

  ```
  echo ${#IPTS[@]}
  ```

+ 显示数组的第一个元素

  ```
  echo ${IPTS[0]}
  ```



## 3-8 转义和引用

+ 特殊字符

  1. #注释
  2. ;分号，用来连接两条命令
  3. \转义符号
  4. 单引号和双引号

+ 转义

  1. 单个字母的转义

     ```
     \n
     \t
     \r
     ```

     

  2. 单个非字母的转义

     ```
     \$
     \"
     \\
     ```

     

+ 引用

  1. 双引号：里面出现变量会替换
  2. 单引号：里面的变量不替换，原样输出
  3. 反引号



## 3-9 特殊符号

+ 引号

  > 单引号：'，包含的变量不会展开
  >
  > 双引号："
  >
  > 反引号：`

+ 括号

  > 圆括号
  >
  > > ()：在子shell中为变量赋值
  > >
  > > ```shell
  > > ( abc=123 )
  > > # 父进程获取不到值
  > > echo $abc
  > > 
  > > #数组
  > > ipt=(ip1 ip2 ip3)
  > > ```
  > >
  > > (())：算数运算
  > >
  > > ```shell
  > > echo $(( 10+20 ))
  > > ```
  > >
  > > $()：执行命令获取结果
  > >
  > > ```shell
  > > cmd1=$(ls)
  > > echo ${cmd1}
  > > ```
  >
  > 方括号
  >
  > > []：测试，test命令的简写
  > >
  > > ```
  > > [ 5 -gt 4 ]
  > > echo $?
  > > ```
  > >
  > > [[]]：let命令的简写
  >
  > 尖括号
  >
  > > <>：大小比较以及输入和输出的重定向
  > >
  > > ```shell
  > > ls > a.txt
  > > ```
  > >
  > > 
  >
  > 花括号
  >
  > > 1. 输出范围
  > >
  > >    ```shell
  > >    # 输出0-9
  > >    echo {0..9}
  > >    ```
  > >
  > > 2. 文件复制 cp /etc/passwd{,.bak}
  > >
  > >    ```shell
  > >    cp -v /etc/passwd /etc/passwd.bak
  > >    
  > >    # 上面命令的简写
  > >    cp -v /etc/passwd{,.bak}
  > >    ```
  > >
  > >    

+ 运算和逻辑符号

  > 算数运算：+ - * / %
  >
  > 比较运算符：> < =
  >
  > 逻辑运算符：&& || !
  >
  > ```shell
  > (( 5 > 4 ))
  > echo $?
  > 
  > (( 5 > 4 && 6 > 5))
  > echo $?
  > 
  > (( 5 > 4 || 6 < 5))
  > echo $?
  > ```

+ 转义字符

  > \n：普通字符转义后有不同功能
  >
  > \\'：特殊字符转义后，当普通字符使用

+ 其它符号

  > #：注释
  >
  > ;：命令分隔符
  >
  > ;;：case语义分隔符
  >
  > ```shell
  > vim /etc/bashrc
  > ```
  >
  > :：空指令，通常用来作占位符
  >
  > .和source命令相同
  >
  > ~：家目录
  >
  > **,：分隔目录**
  >
  > *：通配符
  >
  > ?：条件测试或通配符
  >
  > $：取值符号
  >
  > |：管道符
  >
  > &：后台运行
  >
  > 空格

# 4 运算符

## 4-1 赋值运算符

a=b

## 4-2 算术运算符

运算符：+ - * / ** %

**：乘方



运算：expr(不支持小数)，符号和数字之间要有空格

expr 4 + 5

## 4-3 数字常量

let ${变量名}=${变量值}



0开头是八进制

0x开头是十六进制

## 4-4 双圆括号

介绍：let命令的简化

```shell
(( a = 10 ))
(( a++ ))
echo $(( 10 + 20 ))

# 整数运算用expr 命令执行
num1=$(expr 4 + 19)

#次数num2为"4+5"，shell只有字符串一种数据类型
num2=4+5
```





# 5 测试与判断

## 5-1 退出与退出状态

+ 退出程序命令：exit

  ```shell
  exit 10 # 返回10给shell，非0返回值表示异常退出
  $? # 获取上个命令返回值
  
  #-----------bash脚本内容------------
  #!/bin/bash
  pwd
  exit 125
  
  #-----------执行bash脚本,获取返回值---------
  bash test.sh
  echo $?
  ```

  

## 5-2 测试命令test

+ 检查文件或者比较值

  1. 文件测试：判断文件是否存在、判断文件是否存在且为目录、判断文件是否存在且为普通文件

     ```shell
     # 判断文件是否存在且为普通文件
     test -f /etc/passwd
     echo $?
     
     [ -d /etc/ ]
     echo $?
     
     [ -d /etc/ ]
     echo $?
     
     ```

  2. 整数比较测试

     ```shell
     [ 5 -gt 4 ]
     echo $?
     
     # 如果要使用> <号之类,用两个中括号,不建议这种用法
     [[ 5 > 4 ]]
     echo $?
     ```

  3. 字符串测试

     ```shell
     [ "abc" = "abc" ]
     echo $?
     
     [ "abc" != "ABC"]
     echo $?
     
     [ -z "abc" ]
     echo $?
     ```

     

+ test可以简化为 [] 符号

+ [] 符号拓展写法[[]] 支持 && || < >

## 5-3 使用 if - then 语句

+ 基本用法

  if [ 测试条件成立 ] 或 命令返回值为0

  then 执行响应命令

  fi 结束

+ 示例

  ```shell
  # 跟着判断语句
  if [ $UID = 0 ];then
  	echo " root user ";
  fi
  
  # 跟着命令,如果命令不存在或者执行失败则不执行then
  if pwd;then
  	echo " pwd running";
  fi
  ```

  

## 5-4 使用 if - then - else 语句

+ 基本用法

  if [ 测试条件成立 ]

  then 执行相应命令

  else 测试条件不成立，执行相应命令

  fi 结束

+ 高级用法

  if [ 测试条件成立 ]

  then 执行相应命令

  elif [ 测试条件成立 ]

  then 执行相应命令

  else 测试条件不成立，执行相应命令

  fi 结束

+ 示例代码

  ```shell
  if [ ${USER} = root ]; then
          echo " user root"
          echo ${UID}
  else
          echo "other user"
          echo ${UID}
  fi
  ```

  ```shell
  SCORE=${1}
  if [ ${SCORE} -gt 90 ]; then
          echo "A"
  elif [ ${SCORE} -gt 80 ]; then
          echo "B"
  elif [ ${SCORE} -gt 70 ]; then
          echo "C"
  else
          echo "D"
  fi
  ```

## 5-5 嵌套 if 的使用

+ 基本用法

  >if [ 测试条件成立 ]
  >
  >then 执行相应命令
  >
  >​		if [ 测试条件成立 ]
  >
  >​		then 执行相应命令
  >
  >​		fi
  >
  >fi

+ 代码示例

  ```shell
  #!/bin/bash
  
  
  if [ ${UID} = 0 ]; then
          echo " please run"
          if [ -x ./10.sh ]; then
                  ./10.sh 98
          fi
  
  else
          echo "switch user root"
  fi
  ```



## 5-6 case分支

+ 基本用法

  > case "${变量}" in
  >
  > ​		"情况1")
  >
  > ​			命令...;;
  >
  > ​		“情况2”)
  >
  > ​			命令...;;
  >
  > ​			*)
  >
  > ​			命令...;;
  >
  > esac

+ 示例代码

  ```shell
  #!/bin/bash
  
  
  case "${1}" in
      "start"|"START")
          echo ${0} start....
       ;;
  
      "stop")
      echo ${0} stop...
      ;;
      
      "restart"|"reload")
      echo ${0} restart...
      ;;
      
      *)
      echo "Usage: ${0} {start|stop|restart|reload}"
      ;;
      
  esac
  ```





# 6 循环

## 6-1 for循环

+ 语法

  > for	参数	in	列表
  >
  > do	执行的命令
  >
  > done	封闭一个循环

+ Tips

  1. **列表中包含多个变量，用空格分隔**
  2. 对文本处理，使用文本查看命令取出文本内容
  3. 默认逐行处理文本，如果出现空格当做多行处理

+ 代码示例

  ```shell
  for i in {1..9}
          do
          echo ${i}
  done
  ```

  ```shell
  # 文件批量改名
  for filename in $(ls *.mp3)
  do
          mv ${filename} $(basename ${filename} .mp3).mp4
  done
  ```

+ C语言风格的for循环(很少用到)

  > for((变量初始化；循环判断条件；变量变化))
  >
  > do
  >
  > ​	循环执行的命令
  >
  > done

+ 示例代码

  ```shell
  for (( i=1; i<=10; i++ ))
  do
          echo ${i}
  done
  ```



## 6-2 while 循环

+ 语法

  > while	test测试是否成立
  >
  > do
  >
  > ​	命令
  >
  > done

+ 代码

  ```shell
  a=1
  
  while [ ${a} -lt 10 ]
  do
          echo ${a}
          ((a++))
  done
  ```

  ```shell
  # 无限循环
  while :
  do
          echo always
  done
  ```

  

## 6-3 until 循环

```shell
# 条件为假则一直执行
until [ 5 -lt 4 ]
do
        echo always
done
```



## 6-4 嵌套

```shell
for     script_name in /etc/profile.d/*.sh
do
        echo ${script_name}
        if [ -x ${script_name} ] ; then
                source %{script_name}
        fi
done
```

```shell
for num in {1..9}
do
        if [ ${num} -eq 5 ] ; then
        break
        fi
        echo ${num}
done
```

```shell
for num in {1..9}
do
        if [ ${num} -eq 5 ] ; then
        continue
        fi
        echo ${num}
done
```

## 6-5 处理命令行参数

+ 小知识

  1. 命令行参数用${1}	${2}	...获取
  2. ${0}表示脚本名称
  3. $*和$@表示全部位置参数
  4. $#表示位置参数的数量

+ 代码

  ```shell
  while [ $# -ge 1 ]
  do
          echo $#
          echo "do something "
          shift
  done
  
  ```

  ```shell
  for param in $*
  do
         if [ ${param} = help ]; then
                 echo ${param} ${param}  
         fi
  done
  ```

  

# 7 函数

## 7-1 自定义函数

+ 函数作用范围内的变量

  local 变量名

+ 函数的参数

  ${1} ${2} ... ${n}

+ 示例

  ```shell
  function cdls(){
  cd /
  ls
  }
  
  cdls
  ```

  

  ```shell
  # 可以省略function关键字
  cdls(){
  cd ${1}
  ls
  }
  
  cdls /tmp
  ```

  ```shell
  checkpid()
  {
  		# 仅在函数内部生效的变量
          local i
          for i in $* ; do
                  [ -d "/proc/$i" ] && return 0
          done
  
          return 1
  }
  
  ```

  

## 7-2 系统脚本

+ 系统自建函数库，可以在脚本中引用*/etc/init.d/functions*

+ 自建函数库，使用*source /etc/init.d/functions*

+ 常用的脚本

  > 1. /etc/profile
  > 2. ~/.bashrc
  > 3. ~/.bash_profile
  > 4. /etc/init.d/functions