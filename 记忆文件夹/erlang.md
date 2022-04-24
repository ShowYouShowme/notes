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
-record(person, {name = "", id}). 

start() -> 
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



