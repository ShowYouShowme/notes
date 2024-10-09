# 第一章 基本语法

## 1.1 安装



### 1.1.1 包管理器安装

```shell
sudo apt-get install erlang
```

### 1.1.2 源码安装

```shell
# OTP 19.3 wants OpelSSL 1.0.x.

# step-1 安装openssl
wget https://www.openssl.org/source/openssl-1.0.2r.tar.gz --no-check-certificate
tar -zxvf openssl-1.0.2r.tar.gz 
cd openssl-1.0.2r
./config --prefix=/usr/local/openssl -fpic
make 
make install

# 如果是ubuntu 20.04 需要安装curse
sudo apt-get install libncurses5-dev

# step-3 安装otp 19.3
./configure --prefix=/usr/local/erlang --with-ssl=/usr/local/openssl/ --enable-threads --enable-smp-support --enable-kernel-poll --enable-hipe --without-javac

make 
make install
```





## 1.2 第一个程序

文件名必须是hello_world.erl

```erlang
% hello world program
-module(hello_world).
-export([start/0]).

start()->
    io:fwrite("Hello, world!\n").
```



## 1.3 运行

+ 在erlang的shell中运行

  ```shell
  ~/erlang$ erl
  
  1> c(hello_world).   # 编译
  
  2> hello_world:start(). # 运行
  ```

+ 在命令提示符下运行

  ```shell
  # 使用erlc编译模块 
  $ erlc hello.erl
  
  # 1--前台运行模块,加上 -s init stop 程序运行完会退出，不加不会
  $ erl -noshell -s fac main -s init stop
  
  # 2--前台带参数运行
  $ erl -noshell -s fac main 25
  
  # 加载指定路径并执行其所包含的模块中的函数
  erl -noshell -pa path -s module fun
  ```

  



# 第二章 数据类型

+ Number：包含整数和浮点数
+ Atom：全小写字母，类似其它语言的枚举类型
+ Boolean
+ Bit String：类似C++的Vector\<unsigned char>
+ Tuple
+ Map
+ List：string也是用List表示，类似C语言
+ record：结构体



# 第三章 变量

erlang变量要用大写字母开头命名，变量是不可变的。



使用未定义的变量会报错

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   X = 40, 
   Y = 50, 
   result = X + Y, 
   io:fwrite("~w",[Result]).
```



变量不能二次赋值

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   X = 40, 
   Y = 50, 
   X = 60, 
   io:fwrite("~w",[X]).
```



格式化打印输出

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   X = 40.00, 
   Y = 50.00, 
   io:fwrite("~f~n",[X]), 
   io:fwrite("~e",[Y]).
```



# 第四章 循环



## 4.1 while循环

```erlang
% hello world program

-module(hello_world).
-export([while/1, while/2, start/0]).


while(L) -> while(L, 0).

while([], Acc) -> Acc;

while([First|T], Acc) ->
    io:fwrite("~w\n",[First]),
    while(T, Acc +1).

start() ->
    X = [1,2,3,4],
    while(X).
```





## 4.2 for循环

```erlang
```





# 第五章 if语句



## 5.1 if语句

```erlang
if
condition ->
   statement #1;
true ->
   statement #2
end
```

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   A = 5, 
   B = 6, 
   
   if 
      A == B -> 
         io:fwrite("True"); 
      true -> 
         io:fwrite("False") 
   end.
```





## 5.2 多重表达式

```erlang
if
condition1 ->
   statement#1;
condition2 ->
   statement#2;
conditionN ->
   statement#N;
true ->
   defaultstatement
end
```



```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   A = 5, 
   B = 6, 
   if 
      A == B -> 
         io:fwrite("A is equal to B"); 
      A < B -> 
         io:fwrite("A is less than B"); 
      true -> 
         io:fwrite("False") 
   end.
```



## 5.3 嵌套if语句

```erlang
-module(helloworld). 
-export([start/0]). 

%% 如果没有true，当其它模式都不匹配的时候会报错，具有assert的功能

%% 如果true里面什么也不想做，可以这么写
%% true -> void 模拟 C语言的 if(expr){}   -- 此时没有else
start() -> 
   A = 4, 
   B = 6, 
   if 
      A < B ->
         if 
            A > 5 -> 
               io:fwrite("A is greater than 5"); 
            true -> 
               io:fwrite("A is less than 5")
         end;
      true -> 
         io:fwrite("A is greater than B") 
   end.
```



## 5.4 Case语句

```erlang
case expression of
   value1 -> statement#1;
   value2 -> statement#2;
   valueN -> statement#N
end
```

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   A = 5,
   case A of 
      5 -> io:fwrite("The value of A is 5"); 
      6 -> io:fwrite("The value of A is 6") 
   end.
```

```erlang
    A1 = 50,
    B1 = 100,
    case (A1 > 20) and (B1 > 80) of
        true ->
            io:fwrite("++++~n", []);
        _ ->
            io:fwrite("====~n")
    end.
```



# 第六章 函数



## 6.1 定义函数

```erlang
-module(helloworld). 
-export([add/2,start/0]). 

add(X,Y) -> 
   Z = X+Y, 
   io:fwrite("~w~n",[Z]). 
   
start() -> 
   add(5,6).
```



## 6.2 匿名函数

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   Fn = fun() -> 
      io:fwrite("Anonymous Function") end, 
   Fn().
```

```erlang
% 匿名函数递归, 匿名函数可以直接捕获外部变量
start() ->
	CallBack = fun
                    Test([]) -> 
                        io:fwrite("finished");
                    Test([H|T]) ->
                        io:fwrite("~p ", [H]),
                        Test(T)
    end,
    L1 = [1,2,3,4],
    CallBack(L1).
```



```erlang
%% 类似map，非常简洁
start() -> 
    P = [1,2,3,4],
    Fun = fun 
            Loop([]) -> [];
            Loop([H|T]) -> [2 * H | Loop(T)]
    end,
   io:fwrite("~p~n",[Fun(P)]). %%[2,4,6,8]
```



```erlang
%% 返回fun的函数,用于捕获变量
%% 默认情况下，匿名函数会捕获全部变量,如果只想捕获一部分变量
%% 可以使用全局函数 或者 避免变量重名

	%% 把X捕获进去
	%% 使用场景,lists:filter 的回调函数只有一个参数,如果需要其它状态做处理就可以这样做
    Fun = fun(X)->
        (fun(Y) -> io:format("~w : ~w ~n",[X, Y])end)
    end,
```





## 6.3 函数重载

```erlang
-module(helloworld). 
-export([add/2,add/3,start/0]). 

add(X,Y) -> 
   Z = X+Y, 
   io:fwrite("~w~n",[Z]). 
   
add(X,Y,Z) -> 
   A = X+Y+Z, 
   io:fwrite("~w~n",[A]). 
 
start() ->
   add(5,6), 
   add(5,6,6).
```



## 6.4 保护序列函数

```erlang
-module(helloworld). 
-export([add/1,start/0]). 

add(X) when X>3 -> 
   io:fwrite("~w~n",[X]). 

start() -> 
   add(4).
```



# 第七章 模块



## 7.1 导出

```erlang
-module(helloworld). 
-author("TutorialPoint"). 
-version("1.0"). 
-export([start/0]). 

start() -> 
   io:fwrite("Hello World").
```



## 7.2 导入

```erlang
-module(helloworld). 
-import(io,[fwrite/1]). 
-export([start/0]). 

start() -> 
   fwrite("Hello, world!\n").
```



# 第八章 递归



## 8.1 基本用法

```erlang
% hello world program
-module(hello_world).
-export([start/0]).

fac(N) ->
    if
        N == 0 ->
            1;
        true ->
            N * fac(N - 1)
    end.

start()->
    X = fac(4),
    io:fwrite("~w \n", [X]).
```



## 8.2 实用案例



### 8.2.1 长度递归

```erlang
% hello world program
-module(hello_world).
-export([start/0]).

len([]) -> 0;

len([_|T]) -> 1 + len(T).


start()->
    X = [1,2,3,4],
    Y = len(X),
    io:fwrite("~w\n", [Y]).
```



### 8.2.2 尾递归

```erlang
-module(helloworld).
-export([tail_len/1,tail_len/2,start/0]). 

tail_len(L) -> tail_len(L,0). 
tail_len([], Acc) -> Acc; 
tail_len([_|T], Acc) -> tail_len(T,Acc+1). 

start() -> 
   X = [1,2,3,4], 
   Y = tail_len(X), 
   io:fwrite("~w",[Y]).
```



### 8.2.3 重复

```erlang
% hello world program
-module(hello_world).
-export([start/0]).

duplicate(0, _) ->
    [];

duplicate(N, Term) when N > 0 ->
    [Term | duplicate(N - 1, Term)].

start() ->
    X = duplicate(5,1),
    io:fwrite("~w \n", [X]).
```





### 8.2.4 列表反转

```erlang
-module(helloworld). 
-export([tail_reverse/2,start/0]). 

tail_reverse(L) -> tail_reverse(L,[]).

tail_reverse([],Acc) -> Acc; 
tail_reverse([H|T],Acc) -> tail_reverse(T, [H|Acc]).

start() -> 
   X = [1,2,3,4], 
   Y = tail_reverse(X), 
   io:fwrite("~w",[Y]).
```



# 第九章 数字



## 9.1 整数

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   io:fwrite("~w",[1+1]).
```





## 9.2 浮点数

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   io:fwrite("~f~n",[1.1+1.2]), 
   io:fwrite("~e~n",[1.1+1.2]).
```



# 第十章 字符串



## 10.1 基本用法

```erlang
-module(helloworld). 
-export([start/0]). 

start() ->
   Str1 = "This is a string", 
   io:fwrite("~p~n",[Str1]).
```



## 10.2 常见函数



### 10.2.1 to_lower

```erlang
-module(helloworld). 
-import(string,[to_lower/1]). 
-export([start/0]). 

start() -> 
   Str1 = "HELLO WORLD", 
   Str2 = to_lower(Str1), 
   io:fwrite("~p~n",[Str2]).
```



### 10.2.2 sub_string

```erlang
-module(helloworld). 
-import(string,[sub_string/3]). 
-export([start/0]). 

start() -> 
   Str1 = "hello world", 
   Str2 = sub_string(Str1,1,5), 
   io:fwrite("~p~n",[Str2]).
```



# 第十一章 列表



## 11.1 基本用法

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   Lst1 = [1,2,3], 
   io:fwrite("~w~n",[Lst1]).
```





## 11.2 常见API



### 11.2.1 all

```erlang
-module(hello_world).
-import(lists,[all/2]). 
-export([start/0]). 

start() -> 
   Lst1 = [4,2,8], 
   Predicate = fun(E) -> E rem 2 == 0 end, 
   Status = all(Predicate, Lst1), 
   io:fwrite("~w~n",[Status]).
```



### 11.2.2 any

```erlang
-module(helloworld). 
-import(lists,[any/2]). 
-export([start/0]). 

start() -> 
   Lst1 = [1,2,3], 
   Predicate = fun(E) -> E rem 2 == 0 end,
   Status = any(Predicate, Lst1), 
   io:fwrite("~w~n",[Status]).
```





### 11.2.3 delete

```erlang
-module(helloworld). 
-import(lists,[delete/2]). 
-export([start/0]). 

start() -> 
   Lst1 = [1,2,3], 
   Lst2 = delete(2,Lst1), 
   io:fwrite("~w~n",[Lst2]).
```





# 第十二章 文件



## 12.1 基本用法

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   {ok, File} = file:open("Newfile.txt",[read]),
   Txt = file:read(File,1024 * 1024), 
   io:fwrite("~p~n",[Txt]).
```



## 12.2 常用API

| 方法      | 说明                 |
| --------- | -------------------- |
| open      | 打开文件             |
| write     | 写入文件             |
| file_read | 一次读取文件所有内容 |
| file_size | 获取文件大小         |



# 第十三章 原子

类似于C语言的枚举



命名

+ 全部用小写字母：atom1
+ 使用单引号：'atom_1'



# 第十四章 映射



## 14.1 基本用法

```erlang
% hello world program
-module(hello_world).
-export([start/0]). 

start() -> 
    M1 = #{name =>john, age =>25},
    io:fwrite("~w~n", [map_size(M1)]).
```



## 14.2 常用API



### 14.2.1 get

```erlang
% hello world program
-module(hello_world).
-export([start/0]). 

start() -> 
    List1 = [{"a", 1}, {"b", 2}, {"c", 3}],
    Map1 = maps:from_list(List1),
    io:fwrite("~p~n", [maps:get("a", Map1)]).
```



### 14.2.2 keys

```erlang
% 返回所有key
-module(helloworld). 
-export([start/0]). 

start() -> 
   Lst1 = [{"a",1},{"b",2},{"c",3}], 
   Map1 = maps:from_list(Lst1), 
   io:fwrite("~p~n",[maps:keys(Map1)]).
```



# 第十五章 元组



## 15.1 基本用法

```erlang
-module(helloworld). 
-export([start/0]). 

start() ->
   P = {john,24,{june,25}} , 
   io:fwrite("~w",[tuple_size(P)]).
```



## 15.2 is_tuple

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   P = {john,24,{june,25}} , 
   io:fwrite("~w",[is_tuple(P)]).
```



## 15.3 list_to_tuple

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   io:fwrite("~w",[list_to_tuple([1,2,3])]).
```





## 15.4 tuple_to_list

```erlang
-module(helloworld). 
-export([start/0]). 

start() -> 
   io:fwrite("~w",[tuple_to_list({1,2,3})]).
```



# 第十六章 记录

记录类似C语言的struct



## 16.1 创建记录

```erlang
-module(helloworld). 
-export([start/0]). 

%% 定义类型person,类似C定义结构体
%% struct person {....}
%% name 默认值为"", age默认值为28
-record(person, {name = "", id, age = 28}). 

start() -> 
   %% 创建实例 
   P = #person{name="John",id = 1}.
```





## 16.2 访问记录的值

```erlang
-module(helloworld). 
-export([start/0]). 
-record(person, {name = "", id}). 

start() -> 
   P = #person{name = "John",id = 1}, 
   io:fwrite("~p~n",[P#person.id]), 
   io:fwrite("~p~n",[P#person.name]).
```





## 16.3 更新记录的值

```erlang
-module(helloworld). 
-export([start/0]). 
-record(person, {name = "", id}). 

start() -> 
   P = #person{name = "John",id = 1}, 
   P1 = P#person{name = "Dan"}, 
   
   io:fwrite("~p~n",[P1#person.id]), 
   io:fwrite("~p~n",[P1#person.name]).
```

```erlang
%% 错误的更新方式:  嵌套类型更新数据值 t_battle_pass 成员要写全，否则未写的成员是undefined
NewRole = Role#role{m_battle_pass = #t_battle_pass{info = Info, reward = Reward, open_moment = CurTimestamp} },
    
    
%% 推荐的写法 上面那种写法修改了结果就出问题
    Old_battle_pass = NewRole#role.m_battle_pass,
    New_battle_pass = Old_battle_pass#t_battle_pass{info = NewInfo, reward = NNReward},
    UpdateRole = NewRole#role{m_battle_pass = New_battle_pass },
```





## 16.4 嵌套记录

```erlang
-module(helloworld). 
-export([start/0]). 
-record(person, {name = "", address}). 
-record(employee, {person, id}). 

start() -> 
   P = #employee{person = #person{name = "John",address = "A"},id = 1}, 
   io:fwrite("~p~n",[P#employee.id]).
```



## 16.5 模式匹配

```erlang
-module(record_access). 
-export([start/0]). 
-record(person, {name = "", id,age}). 

start() -> 
    P1 = #person{name = "nash", id = 123, age = 29},
    io:fwrite("P1:~p~n",[P1]),
    %% 快速获取多个变量
    #person{name = Name, id = Id, age = Age} = P1,
    io:fwrite("[Name]:~p, [Id]:~p, [Age]:~p ~n",[Name, Id, Age]).
```



嵌套类型的模式匹配

```erlang
-module(record_access). 
-export([start/0]). 
-record(person, {name = "", address}). 
-record(employee, {person, id}). 

start() -> 
   P = #employee{person = #person{name = "John",address = "A"},id = 1}, 
   #employee{person = #person{name = Name,address = Addr},id = Id} = P,
    %% 或者 不一定要匹配出全部成员
    %% #employee{person = #person{name = Name},id = Id} = P,
   io:fwrite("[Name]:~p, [Addr]:~p, [Id]:~p ~n", [Name, Addr, Id]).
```





# 第十七章 异常



## 17.1 异常分类

+ error：运行时异常，在发生除零错误、匹配运算失败、找不到匹配的函数子句等情况时触发。这些异常的特点在于一旦它们促使某个进程崩溃，Erlang错误日志管理器便会将之记录在案
+ exit：用于通报“进程即将停止”。它们会在迫使进程崩溃的同时将进程退出的原因告知给其他的进程，因此一般不捕获这类异常，exit也在进程正常终止时使用，这时它会令进程退出并通报“任务结束，一切正常”。无论是哪种情况，进程因exit而终止都不算是意外事件，因而也不会被汇报至错误日志管理器
+ throw：用于处理用户自定义的情况。你可以用throw来通报你的函数遭遇了某种意外，也可以用它来完成所谓的非局部返回或是用于跳出深层递归。如果进程没能捕获throw异常，它便会转变成一个原因为nocatch的error异常，迫使进程终止并记录日志



## 17.2 抛出异常

```erlang
throw(SomeTerm)
exit(Reason)
erlang:error(Reason)
```



## 17.3 异常处理语法

异常捕获一般形式

```erlang
try
     some_unsafe_function()
catch
	 oops               -> got_throw_oops;
     throw:Other  -> {got_throw,Other};
     exit:Reason  -> {got_exit,Reason};
     error:Reason -> {got_error,Reason}
end
```



捕获所有异常

```erlang
_:_      -> got_some_exception
```



异常捕获复杂形式

```erlang
try
     some_unsafe_function
of
     0 -> io:format("nothing to do ~n");
     N -> do_something_with(N)
catch
     _:_ -> io:format("some problem")
end
```

此外，还可以增加after段，不管出现什么情况，after的代码一定会被执行。



# 第十八章 宏

和c语言的宏定义类似



```erlang
-module(helloworld). 
-export([start/0]). 
-define(a,1). 

start() -> 
   io:fwrite("~w",[?a]).
```



```erlang
-module(helloworld). 
-export([start/0]). 
-define(macro1(X,Y),{X+Y}). 

start() ->
   io:fwrite("~w",[?macro1(1,2)]).
```



# 第十九章 头文件



## 19.1 案例 一

+ user.hrl

  ```erlang
  -record(person, {name = "", id}).
  ```

+ hello_world.erl

  ```erlang
  % hello world program
  -module(hello_world).
  -export([start/0]). 
  -include("user.hrl").
  
  start()->
      P = #person{name = "John", id = 8},
      io:fwrite("~p~n", [P#person.name]),
      io:fwrite("~p~n", [P#person.id]).
  ```



## 19.2 案例二

+ user.hrl

  ```erlang
  -define(macro1(X, Y), {X+Y}).
  ```

+ hello_world.erl

  ```erlang
  % hello world program
  -module(hello_world).
  -export([start/0]). 
  -include("user.hrl").
  
  start()->
      io:fwrite("~w~n", [?macro1(11,22)]).
  ```

  

# 第二十章 预处理



+ 源文件

  ```erlang
  % hello world program
  -module(hello_world).
  -export([start/0]). 
  -include("user.hrl").
  
  start()->
      io:fwrite("~w~n", [?macro1(11,22)]).
  ```

+ 预处理

  ```shell
  erlc -P hello_world.erl 
  ```

+ 预处理之后的文件

  ```erlang
  -file("hello_world.erl", 1).
  
  -module(hello_world).
  
  -export([start/0]).
  
  -file("user.hrl", 1).
  
  -file("hello_world.erl", 5).
  
  start() ->
      io:fwrite("~w~n", [{11 + 22}]).
  ```



# 第二十章 模式匹配



## 20.1 列表匹配

```erlang
[A,B,C|T] = [1,2,3,4,5,6],
io:format("A: ~w B: ~w C : ~p T : ~p ~n", [A,B,C, T]).
```

```erlang
% 匹配失败,[H|T]意味着至少有一个元素
[H|T]=[]
```



## 20.2 bitstring 匹配



# 第二十一章 Guard



# 第二十二章 BIFS

定义：内置函数



## 22.1 基础用法

```erlang
-module(helloworld). 
-export([start/0]). 

start() ->   
   io:fwrite("~p~n",[tuple_to_list({1,2,3})]), 
   io:fwrite("~p~n",[time()]).
```



## 22.2 常见API

| 函数          | 说明                                                       |
| ------------- | ---------------------------------------------------------- |
| date          | 返回当前系统日期                                           |
| byte_size     | 返回一个位串中包含的字节数                                 |
| element       | 返回元组中的第N个元素                                      |
| float         | 返回特定数字的浮点值                                       |
| get           | 将字典作为列表返回                                         |
| put           | 在字典中放置一个键值对                                     |
| localtime     | 给出系统中的本地日期和时间                                 |
| memory        | 内存的信息                                                 |
| now           | 自1970年1月1日格林威治标准时间00:00开始经过的时间          |
| ports         | 返回本地节点上所有端口的列表                               |
| processes     | 返回与本地节点上当前存在的所有进程相对应的进程标识符的列表 |
| universaltime | 根据世界标准时间(UTC)返回当前日期和时间                    |



# 第二十二章 二进制文件



# 第二十三章 进程

```erlang
-module(helloworld). 
-export([start/0, call/2]). 

call(Arg1, Arg2) -> 
   io:format("~p ~p~n", [Arg1, Arg2]). 
start() -> 
   Pid = spawn(?MODULE, call, ["hello", "process"]), 
   io:fwrite("~p",[Pid]).
```





# 第二十四章  网络编程



## 24.1 udp编程

```erlang
% hello world program
-module(hello_world).
-export([start/0,client/1]). 

start() -> 
   spawn(fun() -> server(4000) end).

server(Port) ->
   {ok, Socket} = gen_udp:open(Port, [binary, {active, false}]), 
   io:format("server opened socket:~p~n",[Socket]), 
   loop(Socket). 

loop(Socket) ->
   inet:setopts(Socket, [{active, once}]), 
   receive 
      {udp, Socket, Host, Port, Bin} -> 
      io:format("server received:~p~n",[Bin]), 
      gen_udp:send(Socket, Host, Port, Bin), 
      loop(Socket) 
   end. 

client(N) -> 
   {ok, Socket} = gen_udp:open(0, [binary]), 
   io:format("client opened socket=~p~n",[Socket]), 
   ok = gen_udp:send(Socket, "localhost", 4000, N), Value = receive 
      {udp, Socket, _, _, Bin} ->
         io:format("client received:~p~n",[Bin]) after 2000 ->
      0 
   end, 
   
gen_udp:close(Socket), 
Value.
```





## 24.2 tcp编程

```erlang
% hello world program
-module(hello_world).
%%% The echo module provides a simple TCP echo server. Users can telnet
%%% into the server and the sever will echo back the lines that are input
%%% by the user.
-export([accept/1]).

%% Starts an echo server listening for incoming connections on
%% the given Port.
accept(Port) ->
    {ok, Socket} = gen_tcp:listen(Port, [binary, {active, true}, {packet, 0}, {reuseaddr, true}]),
    io:format("Echo server listening on port ~p~n", [Port]),
    server_loop(Socket).

%% Accepts incoming socket connections and passes then off to a separate Handler process
server_loop(Socket) ->
    {ok, Connection} = gen_tcp:accept(Socket),
    Handler = spawn(fun () -> echo_loop(Connection) end),
    gen_tcp:controlling_process(Connection, Handler),
    io:format("New connection ~p~n", [Connection]),
    server_loop(Socket).

%% Echoes the incoming lines from the given connected client socket
echo_loop(Connection) ->
    receive
        {tcp, Connection, Data} ->
	    gen_tcp:send(Connection, Data),
	    echo_loop(Connection);
	{tcp_closed, Connection} ->
	    io:format("Connection closed ~p~n", [Connection])
    end.
```



# 第二十五章 分布式编程

每台物理机运行一个Erlang VM，将这些Erlang VM互相连接，就会组成一个集群。运行在每个VM 里面的进程就可以用消息的模式通信。**注意：每一个Erlang VM 都要运行在受信网络，最好是一个局域网。不同的局域网需要用openVpn这样的工具互联。**



## 25.1 原因

+ 性能
+ 可靠性
+ 可拓展性



## 25.2 常用方法

| 函数      | 说明                       |
| --------- | -------------------------- |
| spawn     | 创建新进程并对其进行初始化 |
| node      | 返回本地节点的名称         |
| spawn节点 | 在节点上创建新进程         |
| is_alive  | 判断节点是否处于活动状态   |
| spawnlink | 在节点上创建新的过程链接   |



## 25.3 节点启动

1. 长节点名启动，网络必须配有DNS

   ```shell
   erl -name simple_cache
   ```

2. 短节点名启动，同一子网即可

   ```shell
   erl -sname simple_cache
   ```



## 25.4 节点互联

1. 连接节点

   ```shell
   net_adm:ping('BeiJing@DESKTOP-34T414H').
   ```

2. 查看已经建立连接的节点

   ```shell
   nodes().
   ```



## 25.5 magic cookie

1. 查看cookie

   ```shell
   auth:get_cookie()
   ```

2. 不同的节点配置相同的cookie即可互联，存在文件名为.erlang.cookie的文件里









# 第二十六章 并发



## 26.1 创建进程

```erlang
-module(hello_world).
-export([start/0]). 


start() ->
    spawn(fun() -> server("Hello") end).

server(Message) ->
    io:fwrite("~p~n", [Message]).
```



## 26.2 发送消息

```erlang
-module(helloworld). 
-export([start/0]). 
start() -> 
   Pid = spawn(fun() -> server("Hello") end), 
   Pid ! {hello}. 

server(Message) ->
   io:fwrite("~p",[Message]).
```





## 26.3 接受消息



### 26.3.1 语法

```erlang
receive
Pattern1 [when Guard1] ->
Expressions1;
Pattern2 [when Guard2] ->
Expressions2;
...
End
```



### 26.3.2 案例

```erlang
-module(helloworld). 
-export([loop/0,start/0]). 

loop() ->
   receive 
      {rectangle, Width, Ht} -> 
         io:fwrite("Area of rectangle is ~p~n" ,[Width * Ht]), 
         loop(); 
      {circle, R} ->
      io:fwrite("Area of circle is ~p~n" , [3.14159 * R * R]), 
      loop(); 
   Other ->
      io:fwrite("Unknown"), 
      loop() 
   end. 

start() ->
   Pid = spawn(fun() -> loop() end), 
   Pid ! {rectangle, 6, 10}.
```



## 26.4 超时



### 26.4.1 语法

```erlang
receive 
Pattern1 [when Guard1] -> 
Expressions1; 

Pattern2 [when Guard2] ->
Expressions2; 
... 
after Time -> 
Expressions 
end
```



### 26.4.2 案例

```erlang
-module(helloworld). 
-export([sleep/1,start/0]). 

sleep(T) ->
   receive 
   after T -> 
      true 
   end. 
   
start()->
   sleep(1000). %休眠1000毫秒
```



## 26.5 选择性接受

```erlang
receive 
Pattern1 [when Guard1] ->
Expressions1; 

Pattern2 [when Guard1] ->
Expressions1; 
... 
after 
Time ->
ExpressionTimeout 
end
```



# 第二十七章 性能

+ Funs非常快
+ 使用++运算符需要小心
+ 字符串处理不当会很慢
+ BEAM是一个基于堆栈的字节码虚拟机



# 第二十八章 驱动程序

主要讲解erlang如何调用动态链接库，其实完全可以使用进程间通信接入sdk。



# 第二十九章 网络编程

利用inets库来构建web服务。



```erlang
-module(helloworld). 
-export([start/0]). 

start() ->
   inets:start(), 
   Pid = inets:start(httpd, [{port, 8081}, {server_name,"httpd_test"}, 
   {server_root,"D://tmp"},{document_root,"D://tmp/htdocs"},
   {bind_address, "localhost"}]), io:fwrite("~p",[Pid]).
```



# 第三十章 OTP编程



## 30.1 gen_server

通用服务框架

简介

```erlang
gen_server module            Callback module
-----------------            ---------------
gen_server:start
gen_server:start_link -----> Module:init/1

gen_server:stop       -----> Module:terminate/2

gen_server:call
gen_server:multi_call -----> Module:handle_call/3

gen_server:cast
gen_server:abcast     -----> Module:handle_cast/2

-                     -----> Module:handle_info/2

-                     -----> Module:terminate/2

-                     -----> Module:code_change/3
```





最简单的示例

```erlang
% erlang 实现的echo服务,基于TCP协议
-module(tr_server).
-behaviour(gen_server).
-define(SERVER, ?MODULE).
-export([start/0, get_count/0, stop/0]).
% gen_server callbacks
-export([init/1, handle_call/3, handle_cast/2, handle_info/2]).
-record(state, {port, lsock, request_count = 0}). % 保存进程状态

start() ->
    Port = 1085,
    gen_server:start({local,?SERVER}, ?MODULE, [Port], []). % 单独启动的服务, 成功返回{ok,Pid} 可以利用NAME 或者Pid来rpc调用接口

% gen_server:start 会回调该函数初始化服务
init([Port]) ->
    {ok, LSock} = gen_tcp:listen(Port, [{active, true}, {reuseaddr, true}]),
    % 第三个参数是超时,0表示立即超时,handle_info 会被调用
    {ok, #state{port = Port, lsock = LSock}, 0}.

handle_call(get_count, _From, State) ->
    {reply, {ok, State#state.request_count}, State}.

handle_cast(stop, State) ->
    {stop, normal, State}.

handle_info(Info, State) ->
    case Info of
        timeout ->
            io:fwrite("[receive info]: ~p ~p ~n", [Info, State]),
            #state{lsock = LSock}=State,
            {ok, _Sock} = gen_tcp:accept(LSock),
            {noreply, State};
        {tcp, Connect, Message} ->
            io:fwrite("[receive info]: ~p !~n", [Message]),
            gen_tcp:send(Connect, Message),
            RequestCount = State#state.request_count,
            {noreply, State#state{request_count = RequestCount +1}};
        {tcp_closed, Connect} ->
            io:fwrite("[receive info]: connection is closed !~n", []),
            gen_tcp:close(Connect),
            {noreply, State};
        Other ->
            io:fwrite("[receive info]: unexpected message ~p !~n", [Other]),
            {noreply, State}
    end.


% 对外暴露的API 接口, 如果有多个实例,可以传入Pid而不是NAME
get_count() ->
    gen_server:call(?SERVER, get_count).


stop()->
    gen_server:cast(?SERVER, stop).
```



## 30.2 gen_event

事件处理框架。正常一个事件管理器对应一个文件；一个事件处理器对应一个文件；一个应用中可以存在多个事件处理器，类似web里面的中间件！

简介

```erlang
gen_event module                   Callback module
----------------                   ---------------
gen_event:start
gen_event:start_link       ----->  -

gen_event:add_handler
gen_event:add_sup_handler  ----->  Module:init/1

gen_event:notify
gen_event:sync_notify      ----->  Module:handle_event/2

gen_event:call             ----->  Module:handle_call/2

-                          ----->  Module:handle_info/2

gen_event:delete_handler   ----->  Module:terminate/2

gen_event:swap_handler
gen_event:swap_sup_handler ----->  Module1:terminate/2
                                   Module2:init/1

gen_event:which_handlers   ----->  -

gen_event:stop             ----->  Module:terminate/2

-                          ----->  Module:code_change/3
```



示范代码一

```erlang
-module(sc_event_logger).
-behaviour(gen_event).
-record(state, {}).
-export([start/0, add_handler/0, delete_handler/0, create/2, lookup/1, add_handler/2]).
-export([init/1, handle_event/2, handle_call/2,
         handle_info/2]).
-define(SERVER, ?MODULE).
start() ->
    gen_event:start({local, ?SERVER}). % 创建event manager,一个event manager可以加入多个handler

add_handler(Handler, Args) ->
    gen_event:add_handler(?SERVER, Handler, Args). % 添加一个Handler,会回调Handler的init函数

add_handler() ->
    gen_event:add_handler(?SERVER, ?MODULE, []).

delete_handler() ->
    gen_event:delete_handler(?SERVER, ?MODULE, []).

init([]) ->
    io:fwrite("call fun init to do something...~n"),
    {ok, #state{}}.

handle_event(Event, State)->
    case Event of
        Other ->
            io:fwrite("[event]:~p~n",[Other]),
            {ok, State}
    end.

handle_call(Request, State)->
    case Request of
        Other ->
            io:fwrite("[call]:~p~n", [Other]),
            Reply = {ok, "call success!"},
            {ok, Reply, State}
    end.

handle_info(Info, State)->
    io:fwrite("[info]:~p~n",[Info]),
    {ok, State}.

create(Key, Value) ->
    gen_event:notify(?SERVER, {create, {Key, Value}}). % 发送消息到全部加入到event manager的Handler

lookup(Key) ->
    gen_event:notify(?SERVER, {lookup, Key}).
```



示范代码二

sc_event_logger.erl

```erlang
-module(sc_event_logger).
-behaviour(gen_event).
-export([add_handler/0, delete_handler/0]).
-export([init/1, handle_event/2, handle_call/2,
handle_info/2, code_change/3, terminate/2]).
-record(state, {}).

add_handler() ->
    sc_event:add_handler(?MODULE, []).

delete_handler() ->
    sc_event:delete_handler(?MODULE, []).

init([]) ->
    error_logger:info_msg("call handler:init ~n", []),
    {ok, #state{}}.

handle_event({create, {Key, Value}}, State) ->
    error_logger:info_msg("create(~p, ~p)~n", [Key, Value]),
    {ok, State}.

handle_call(_Request, State) ->
    Reply = ok,
    {ok, Reply, State}.

handle_info(_Info, State) ->
    {ok, State}.

terminate(_Reason, _State) ->
    ok.

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.
```

sc_event.erl

```erlang
%%%==============================================
%%% 事件管理器,负责启动进程、封装常见API
%%%==============================================

-module(sc_event).
-export([start/0, add_handler/2, delete_handler/2, lookup/1, create/2,replace/2, delete/1]).
-define(SERVER, ?MODULE).

start() ->
    gen_event:start({local, ?SERVER}).

add_handler(Handler, Args) ->
    gen_event:add_handler(?SERVER, Handler, Args).

delete_handler(Handler, Args) ->
    gen_event:delete_handler(?SERVER, Handler, Args).

create(Key, Value) ->
    gen_event:notify(?SERVER, {create, {Key, Value}}).

```

test.erl

```erlang
main() ->
sc_event:start(),
sc_event_logger:add_handler(),
sc_event:create("Name", "Peter"),
sc_event_logger:delete_handler(),
sc_event:create("Name", "Peter").
```





## 30.3 gen_fsm

有限状态机，和gen_server类似，不确定用那个时用gen_server

1. 文档：https://www.erlang.org/docs/19/man/gen_fsm.html

2. 简介

   ```erlang
   % 有限状态机，和gen_server对比，它不仅拥有数据，还有状态
   
   gen_fsm module                    Callback module
   --------------                    ---------------
   gen_fsm:start
   gen_fsm:start_link                -----> Module:init/1
   
   gen_fsm:stop                      -----> Module:terminate/3
   
   gen_fsm:send_event                -----> Module:StateName/2
   
   gen_fsm:send_all_state_event      -----> Module:handle_event/3
   
   gen_fsm:sync_send_event           -----> Module:StateName/3
   
   gen_fsm:sync_send_all_state_event -----> Module:handle_sync_event/4
   
   -                                 -----> Module:handle_info/3
   
   -                                 -----> Module:terminate/3
   
   -                                 -----> Module:code_change/4
   ```

3. 示例代码

   ```erlang
   -module(code_lock). 
   -define(NAME, code_lock).
   -behaviour(gen_fsm). 
   
   -export([start/1, button/1, stop/0]). 
   
   -export([
   	init/1, 
   	locked/2, 
   	open/2, 
   	handle_sync_event/4, 
   	handle_event/3, 
   	handle_info/3, 
   	terminate/3, 
   	code_change/4]). 
   
   start(Code) -> 
   	gen_fsm:start({local, ?NAME}, ?MODULE, Code, []). 
   
   button(Digit) -> 
   	gen_fsm:send_event(?NAME, {button, Digit}). 
   
   stop() -> 
   	Reply = gen_fsm:sync_send_all_state_event(?NAME, stop),
   	io:fwrite("Reply is : ~p ~n", [Reply]).
   
   init(Code) -> 
   	do_lock(), 
   	Data = #{code => Code, remaining => Code}, 
   	{ok, locked, Data}. 
   
   locked({button, Digit}, Data0) -> 
   	io:fwrite("data:~p~n",[Data0]),
   	case analyze_lock(Digit, Data0) of 
   		{open = StateName, Data} -> 
   			{next_state, StateName, Data, 10000}; 
   		{StateName, Data} -> 
   			{next_state, StateName, Data} 
   	end. 
   
   open(timeout, State) -> 
   	io:fwrite("call open with timeout!~n", []),
   	do_lock(), 
   	{next_state, locked, State}; 
   open({button,_}, Data) -> 
   	io:fwrite("call open normal!~n", []),
   	{next_state, locked, Data}. 
   
   % handle_sync_event(stop, _From, _StateName, Data) -> 
   % 	{stop, normal, ok, Data}. 
   
   handle_sync_event(Event, From, StateName, StateData) ->
   	io:fwrite("Event:~p From:~p, StateName:~p, StateData:~p ~n",[Event, From, StateName, StateData]),
   	Reply = "This is reply",
   	{reply,Reply,StateName,StateData}.
   handle_event(Event, StateName, Data) -> 
   	{stop, {shutdown, {unexpected, Event, StateName}}, Data}. 
   handle_info(Info, StateName, Data) -> 
   	{stop, {shutdown, {unexpected, Info, StateName}}, StateName, Data}. 
   
   terminate(_Reason, State, _Data) -> 
   	State =/= locked andalso do_lock(),
   	ok. 
   code_change(_Vsn, State, Data, _Extra) -> 
   	{ok, State, Data}.
   
   analyze_lock(Digit, #{code := Code, remaining := Remaining} = Data) -> 
   	io:fwrite("[Remaining]:~p~n",[Remaining]),
   	case Remaining of 
   		Digit -> 
   			io:fwrite("[Digit]:~p~n",[Digit]),
   			do_unlock(), 
   			{open, Data#{remaining := Code}}; 
   		% [Digit|Rest] -> 
   		% % Incomplete 
   		% 	io:fwrite("[Digit|Rest]:~p~n",[Digit|Rest]),
   		% 	{locked, Data#{remaining := Rest}}; 
   		_Wrong -> 
   			io:fwrite("_Wrong:~p~n",[_Wrong]),
   			{locked, Data#{remaining := Code}} 
   	end. 
   do_lock() -> 
   	io:format("Lock~n", []). 
   do_unlock() -> 
   	io:format("Unlock~n", []).
   
   ```




## 30.4 supervisor

监督者是进程管理工具。负责其子进程的启动，停止和监视。监督者的基本思路是，保持其子进程能正常运行，并在必要时重新启动子进程。类似pm2。

示例代码

```erlang
-module(sc_sup).

-behaviour(supervisor).

-export([start_link/0,
         start_child/2
        ]).

-export([init/1]).

-define(SERVER, ?MODULE).

start_link() ->
    supervisor:start_link({local, ?SERVER}, ?MODULE, []).

start_child(Value, LeaseTime) ->
    supervisor:start_child(?SERVER, [Value, LeaseTime]).

init([]) ->
    Element = {sc_element, {sc_element, start_link, []},
               temporary, brutal_kill, worker, [sc_element]},
    Children = [Element],
    RestartStrategy = {simple_one_for_one, 0, 1},
    {ok, {RestartStrategy, Children}}.
```





子进程规范

Procs = [{cowboy_clock, {cowboy_clock, start_link, []},permanent, 5000, worker, [cowboy_clock]}]

子进程规范有6个元素组成：{ID,Start,Restart,Shutdown,Type,Modules}

ID：是一个用于在系统内部标识各规范的项式，简单起见，此处采用的是模块名

Start：是一个用于启动进程的三元组{Module,Function,Arguments}，Module是模块名，Function是函数名，Arguments是函数的调用参数列表

Restart：用于指明子进程发生故障时是否需要重启。permanent 子进程总会被重启；temporary 子进程从不会被重启；transient 子进程只有当其被异常终止时才会被重启，即，退出理由不是 normal 。

Shutdown：用于指明如何终止进程。如果取值为一个整数，表示终止进程时应采用软关闭策略，给进程留出一段自我了断的时间(以毫秒为单位)，如果进程未能在指定时间内自行退出，将被无条件终止；如果取值为brutal_kill，表示在关闭监督进程时立即终止子进程；如果取值为infinity，主要用于子进程本身也同为监督者的情况，表示应给予子进程充分的时间自行退出。

Type：用于表示进程是监督者(supervisor)还是工作者(worker)。

Modules：列出该进程所依赖的模块。这部分信息仅用于在代码热升级时告知系统该以何种顺序升级各个模块，一般来说，只需列出子进程的主模块。



监督者重启策略

init/1回调函数的返回值的格式为{ok,{RestartStrategy,Children}}，其中Children是若干子进程规范组成的一个列表，RestartStrategy只是一个三元组{How,Max,Within}，此处它的值是{one_for_one, 10, 10}。

How取值为one_for_one，表示一旦有子进程退出，监督者将针对该进程，且仅针对该进程进行重启。该重启操作不会影响同时运行的其他进程。

one_for_one策略：给监督者静态指派的永久子进程会随监督者的启动而启动并在监督者的生命周期结束时退出。

simple_one_for_one策略：监督者只能启动一种子进程，但却可以启动任意多个，它所有的子进程都是运行时动态添加的，监督者本身在启动时不会启动任何子进程。动态添加子进程只需调用简化版supervisor:start_child/2函数，令监督者启动新的子进程。其他类型(非simple_one_for_one)的监督者在动态添加子进程时，必须将完整的子进程规范传递给start_child/2，例如：supervisor:start_child(?MODULE,{Mod, {Mod, start_link, Args},transient, 100, worker, [Mod]}),

Max和Within这两个值是相互关联的：它们共同确定了重启频率。Max指定的是最大重启次数，Within指定的是时间片，这里Max = 10，Within = 10，表示监督者最多可以在10秒内重启子进程10次，一旦超过限制，监督者都会在终止所有子进程后自我了断，并顺着监督者树向上汇报故障信息。如果这两个值分别取值为0和1，表示目前不启动自动重启，因为自动重启会妨碍我们发现代码中的潜在的问题。
