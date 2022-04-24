# 第一章 基本语法

```erlang
% hello world program
-module(hello_world).
-export([start/0]).

start()->
    io:fwrite("Hello, world!\n").
```

运行

```shell
~/erlang$ erl

1> c(hello_world).   # 编译

2> hello_world:start(). # 运行
```



# 第二章 数据类型

+ Number：包含整数和浮点数
+ Atom
+ Boolean
+ Bit String
+ Tuple
+ Map
+ List



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
end.
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
end.
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
end.
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

