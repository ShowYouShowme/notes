# 第一章 课程介绍

## 1-1 课程介绍

### 为什么C/C++

+ 流行的语言，学习人员多
+ 高性能，对于嵌入式设备则是省电
+ 大量第三方库



### C/C++ 应用场景

+ 嵌入式系统
+ 网络游戏
+ 防火墙、杀毒软件
+ 人工智能
+ 工业级应用
+ 手机APP
+ 云计算



### C、C++、JAVA、C#的区别

+ C++与C的性能相差在正负5%
+ C# 托管代码
+ java基于java虚拟机



### C/C++ 开源第三方库

+ 各种三维游戏引擎
+ 音视频编码解码ffmpeg
+ opencv视频识别库
+ QT跨平台界面和应用库，绝大部分嵌入式设备都支持





### 为什么要Lua + C/C++

+ C++的缺点：编译慢，调试难，学习难度大
+ Lua优点：
  1. 最快的脚本语言
  2. 可以编译调试
  3. 与C/C++结合容易
  4. Lua是对性能有要求的必备脚本



### Lua的应用

+ 魔兽世界、愤怒的小鸟等游戏的任务脚本和后端服务器
+ AlphaGo
+ 视频服务器、入侵检测系统脚本、防火墙脚本

## 1-2 环境准备和编译

### 开发环境准备

***

+ [下载lua5.1.5](http://www.lua.org/ftp/lua-5.1.5.tar.gz)
+ 安装VS2013



### Lua编译

***

+ 编译为动态库
+ 建立Lua编译器项目
+ 编译Lua库为了以后对其拓展



### Lua编译步骤

***

+ 创建dll空项目，将Lua源码复制到项目路径下，并添加到项目里
+ 注视掉`lua.c`和`luac.c`里面的main函数
  1. lua.c是lua的解释器
  2. luac.c是lua的编译器，能将源码编译成字节码
+ 设置编译输出路径
+ 设置输出导入库路径
+ 预处理添加<span style="color:violet">LUA_BUILD_AS_DLL</span>宏



### 创建Lua与C++结合的项目

+ 创建vs2013项目，配置使用lua动态库
+ C++载入main.lua脚本文件

```c++
extern "C"
{
#include <lua.h>
#include <lualib.h>
#include <lauxlib.h>
}
#include <stdio.h>
int main(int argc, char* argv[])
{
    lua_State *L = lua_open();
    luaopen_base(L);//打开基本库
    luaL_loadfile(L, "main.lua");//载入文件
    lua_pcall(L, 
        0,//参数个数 
        0, //返回值个数
        0);//错误函数
    getchar();
    return 1;
}
```



# 第二章 Lua基本语法

## 2-1 Lua变量和基础数据类型

### Lua变量

+ 全局变量 a = 10，**尽量不用全局变量**

  ```lua
  -- main.lua
  a = 10 --全局变量
  print(a)
  
  dofile("test.lua")--类似C++的include
  
  
  --test.lua
  print(a) --可以访问在main.lua文件里定义的全局变量
  ```

  全局变量的缺陷

  + 互相引用难以控制生命周期
  + 容易写错，用一个变量表示不同值
  + 空间不释放

+ **本地变量 local b = 25，保证及时的垃圾回收**



### Lua基础数据类型

+ Nil

  + 表示没有数据的值
  + 全局变量设置为nil会垃圾回收

  ```lua
  local a = nil
  print(type(a))
  ```

+ Booleans：除了false和nil为假，其它值都是真，**0是真**

  ```lua
  local a = true
  print(type(a))
  ```

+ Numbers：Lua没有整数，都是64位double，tonumber：字符串转换为number

  ```lua
  local a = 123
  local b = tonumber("1001")
  print(a + b)
  
  local c = tonumber(true) --无法将boolean转换为number
  print(type(c))
  ```

+ Strings

  + tostring：Number转换为string

  + [[]]多行字符串赋值 ：用lua做配置，语言包，预先设置值，手册应用

    ```lua
  local html = [[
    <html>
  
    </html>
  ]]
    print(html)
    ```
  
  + 与C语言一样的转义
  
    ```lua
    html = "test\ttable\n"
    print(html)
    ```
  
  + 字符串拼接(**不能拼接nil**)：..
  
    ```lua
    local a = 123
    local html = "test1" .. "test2" .. a --可以拼接整数，不能拼接nil
    print(html)
    ```
  
  + 字符串处理<br/>a. 长度：string.len<br/>b. 子串：string.sub(str,3,5)<br/>c. 查找：string.find()，返回[start,end]<br/>d. 替换：string.gsub() 源字符串不变
  
    ```lua
    local html = "abcdefg"
    
    print("len:" .. string.len(html))
    
    print(string.sub(html,3,5)) -- [3,5] 下标从1开始，闭区间
    
    local b, e = string.find(html,"fg") --支持正则表达式
    print("begin:" .. b.. ",end:" .. e)
    
    local s = string.gsub(html,"fg","123") --支持正则表达式，不改变原来值
    print("s:" .. s)
    print("html:" .. html)
    ```

## 2-2 Lua条件判断和循环语句

### if 条件语句

```lua
if conditions then
    then-part
elseif conditions then
    elseif-part
else
    else-part
end
```

示例

```lua
if (1==1 and 1 == 3 or 3 == 3) then
    print("1==1")
elseif 2 == 2 then
    print("in else")
end
```



### while 循环语句

+ 代码示例

  ```lua
  while condition do
  	statements
  end
  ```

+ break退出循环

```lua
local i = -5
while i < 0 do
    print("i = " .. i)
    i = i + 1
    if i == -2 then
        print("break while")
        break
    end
end
```



### repeat 循环语句

```lua
local i = 100
repeat
    i = i + 1
    print("i = " .. i)
until i > 110
```

### for 循环语句

+ 数值循环

  ```lua
  for var=from,to,step do
  	loop-part
  end
  
  for i=1,5,2 do
      print("i = " .. i)
  end
  ```

+ 泛型循环：paris遍历全部，ipairs遍历数组

  ```lua
  local days = {"Sun", "Mon", "Tue"}
  for i,v in ipairs(days) do
      print(i .. ":" .. v)
  end
  
  
  local tab = {[1] = "A", [2] = "B", [4] = "D"}
  for i,v in pairs(tab) do
      print(i .. ":" .. v)
  end
  ```

  

## 2-3 Lua表和函数语法

### 表的处理

***

+ 表的大小 table.getn(t1)
+ 插入 table.insert(a,pos,line)，不传pos相当于push_back
+ 删除 table.remove(a,pos)，不传pos相当于pop_back

数组示例

```lua
local tab1 = {"001", "002", "003"}
for i,v in ipairs(tab1) do
    print("value = " .. v)
end

print("====== insert ==========")
-- 指定插入位置
table.insert(tab1,1,"002-2")
for i,v in ipairs(tab1) do
    print("value = " .. v)
end

--不指定插入位置
table.insert(tab1,"0007")
for i,v in ipairs(tab1) do
    print("value = " .. v)
end
```

```lua
local tab1 = {"001", "002", "003"}
-- 指定删除位置
table.remove(tab1,1)
for i,v in ipairs(tab1) do
    print("value = " .. v)
end

print("++++++")
-- 不指定删除位置
table.remove(tab1)
for i,v in ipairs(tab1) do
    print("value = " .. v)
end
```

map示例

```lua
-- 插入、删除和遍历
local tab2 = {id = 123, age = 20}
tab2["name"] = "xiaoming" --插入
tab2["id"] = nil --删除
for key,value in pairs(tab2) do
    print("key:" .. key .. ",value:" .. value)
end
```



二维数组

```lua
--二维数组
local tab3 = {}
tab3[1] = {"name1","name2"}
tab3[2] = {"value1","value2"}

for k,v in ipairs(tab3) do
    for k2, v2 in ipairs(v) do
        print("k2:" .. k2 .. ",v2:" .. v2)
    end
end
```





### Lua函数

***

+ 普通参数

  ```lua
  function test(param1, param2)
  ```
  
  ```lua
  function test(p1,p2)--lua的参数可以不传
      print(p1)
      if p1 == nil then
          p1 = "001"
      end
      
      if p2 == nil then
          p2 = "002"
      end
      
      print("p1:" .. p1 .. ",p2:" .. p2)
      print("in test function")
  end
  
  test(123)
  ```

+ 可变参数--建议不使用

  ```lua
  function test(...)
  
  function test(param1,...)
  	print(arg.n)
  end
  ```

  示例
  
  ```lua
  function test(...)
      local len = table.getn(arg)
      print("arg len is:" .. len)
      
      for a = 1,len do
          print("arg=" .. arg[a])
      end
      return 1,"name"
  end
  
  local re, n = test(123,"name")
  print("re = " .. re .. ",n = " .. n)
  ```
  
  函数与变量
  
  ```lua
  --函数传给变量
  local event = function(p1) --类似js的方式
      print("event = " .. p1)
  end
  event("key")
  
  function test(...)
      return 1,"name"
  end
  
  
  local func1 = test
  local re, n = func1(123,"name")
  ```
  
  函数覆盖--不建议使用
  
  ```lua
  function test(...)
      local len = table.getn(arg)
      print("arg len is:" .. len) 
      
      for a = 1,len do
          print("arg=" .. arg[a])
      end
      return 1,"name"
  end
  
  function test(...) -- 覆盖之前的函数
      return 2233,"LoveLua"
  end
  
  local re, n = test(123,"name")
  print("re = " .. re .. ",n = " .. n)
  ```

 

# 第三章 Lua调用C++

## 问题

1. C++ 里如何获取Lua传入的参数？
2. C++ 里如何传参数给Lua？

```c++
int CTest(lua_State *L)//固定格式
{
    printf("in CTest");
    return 0;//返回给lua的参数个数
}

lua_register(L, "CTest", CTest);//注册
```

## 3-1 参数类型检查

```c++
//检查lua传入的参数类型是否正确
int CTestTable(lua_State *L)
{
    luaL_checktype(L, 1, LUA_TTABLE);//类型检查,失败代码不再执行
    if (lua_type(L, 2) != LUA_TNUMBER)//类型检查,失败代码继续执行
    {
        printf("param 2 is not number!\n");
    }
    lua_getfield(L, 
        1,//table在栈中的位置 
        "name");
    printf("name = %s \n", lua_tostring(L, -1));
    return 0;
}
```

```lua
local tab = {["name"] = "xiaoming", ["age"] = "22", ["id"] = "007"}
local size = 108
CTestTable(size, size)
```

## 3-2 c++获取Lua传入的参数

1. 数字、布尔值、字符串

   ```c++
   //C++ 代码
   int CTest(lua_State *L)//固定格式
   {
       printf("in CTest:");
       // 获取 lua传入的参数
       size_t len;
       const char* name = lua_tolstring(L, 
                                       1, //栈底
                                       &len);
       int age = lua_tonumber(L, 2);
       bool is = lua_toboolean(L, 3);
       printf("lua name:%s, age = %d is=%d\n", name, age,is);
       return 0;//返回给lua的参数个数
   }
   ```

   ```lua
   --lua代码
   CTest("lua string",123,false)
   ```

2. 数组

   ```c++
   int CTestArr(lua_State *L)
   {
       printf("in CTestArr:");
       //获取数组长度
       int len = luaL_getn(L, 1);
       for (auto i = 1; i <= len; ++i)
       {
           lua_pushnumber(L, i);//push index
           lua_gettable(L, 1);//pop index push table[index]
           size_t size;
           printf("%s\n", lua_tolstring(L, -1, &size));//这个函数只取值不出栈
           lua_pop(L, 1);//pop 
       }
       return 0;
   }
   
   lua_register(L, "CTestArr", CTestArr);
   ```

   ```lua
   local arr = {"A001","A002","A003","A004"}
   CTestArr(arr)
   ```

3. Map

   **lua_next(L,3)**

   + 先从栈顶弹出一个key
   + 从栈指定位置的table里去下一对key-value，先将key入栈再将value入栈
   + 如果第二步成功则返回非0值，否则返回0，并且不向栈中压入任何值

   **遍历Map**

   ```c++
   int CTestTable(lua_State *L)
   {
       lua_pushnil(L); //lua_next先弹出一个key
       while (lua_next(L,1) != 0 )
       {
           //push key, push value
           printf("key = %s \n", lua_tostring(L, -2));
           printf("value = %s\n", lua_tostring(L, -1));
           lua_pop(L, 1);
       }
       return 0;
   }
   ```

   ```lua
   local tab = {["name"] = "xiaoming", ["age"] = "22", ["id"] = "007"}
   CTestTable(tab)
   ```

   **取Map某个属性**

   ```c++
   int CTestTable(lua_State *L)
   {
       lua_getfield(L, 
           1,//table在栈中的位置 
           "name");
       printf("name = %s \n", lua_tostring(L, -1));
       lua_pop(L, 1);
       return 0;
   }
   ```

   ```lua
   local tab = {["name"] = "xiaoming", ["age"] = "22", ["id"] = "007"}
   CTestTable(tab)
   ```

## 3-3 C++返回值给Lua

### 返回普通类型

```c++
int CTestRe(lua_State *L)
{
    lua_pushstring(L, "return value");
    return 1;//lua那边的返回值个数
}
```

```lua
local re = CTestRe()
print("re:" .. re)
```

### 返回表

#### 示例一

***

```c++
int CTestRe(lua_State *L)
{
    lua_newtable(L);
    //插入key 再插入value
    lua_pushstring(L, "name");
    lua_pushstring(L, "xiaoming");
    //将值写入表中
    lua_settable(L, -3);//插入了两个值
    return 1;//lua那边的返回值个数
}
```

```lua
local re = CTestRe()
print("re:" .. re["name"])
```

#### 示例二

****

```c++
int CTestRe(lua_State *L)
{
    //lua_pushstring(L, "return value");

    lua_newtable(L);
    //插入key 再插入value
    lua_pushstring(L, "name");
    lua_pushstring(L, "xiaoming");
    //将值写入表中
    lua_settable(L, -3);//插入了两个值 这个函数会出栈

    lua_pushstring(L, "age");
    lua_pushnumber(L, 21);
    lua_settable(L, -3);
    return 1;//lua那边的返回值个数
}
```

```lua
local re = CTestRe()
print("name:" .. re["name"])
print("age:" .. re["age"])
```



# 第4章 C++调用Lua

## 4-1 c++给lua传递变量和访问lua的全局变量

### 访问Lua全局变量

***
#### 访问Lua基础数据类型

```c++
//在lua_pcall之后才能访问lua变量
lua_getglobal(L, "width");//把符号压入栈
int width = lua_tonumber(L, -1);
lua_pop(L, 1);//弹出一个元素
printf("width = %d\n", width);
```

```lua
width = 1920
```

#### 访问Lua表

```c++
//在lua_pcall之后才能访问lua变量
lua_getglobal(L, "conf");//将conf压入栈

lua_getfield(L, -1, "titlename");//-1 表示conf的位置
printf("title = %s \n", lua_tostring(L, -1));
lua_pop(L, 1);//弹出一个元素

//可以把这3行用宏定义或者函数实现
lua_getfield(L, -1, "height");
printf("height = %f\n", lua_tonumber(L, -1));
lua_pop(L, 1);

lua_pop(L, 1);//弹出表
```

```lua
conf = 
{
    ["titlename"] = "first Lua",
    ["height"] = 1080
}
```



### C++ 给Lua传递全局变量

***
#### 传递基础数据类型

```c++
//在调用luaL_loadfile之前
lua_pushstring(L, "Hello");
lua_setglobal(L, "test");//会出栈
```

```lua
print("test:" .. test)
```

#### 传递表

```c++
//C++给Lua传递表
lua_newtable(L);
lua_pushstring(L, "name");
lua_pushstring(L, "xiaoming");
lua_settable(L, -3);//这行会出栈

lua_pushstring(L, "age");
lua_pushnumber(L, 20);
lua_settable(L, -3);

lua_setglobal(L, "person");//全局变量名
```

```lua
print("person name is:" .. person["name"] .. ",age is:" .. person["age"])
```



## 4-2 c++调用lua函数（基础调用）

注意：

1. 堆栈恢复
2. 多线程互斥，建议每个线程用一个独立的lua_state

```c++
lua_getglobal(L, "event");
lua_pcall(L,
          0,//参数个数
          0,//返回值个数
          0);
```

```lua
function event()
    print("c++ call lua function")
end
```



## 4-3 C++调用Lua函数传递参数

### 传递基础数据类型
```c++
printf("----top is %d \n", lua_gettop(L));
lua_getglobal(L, "event");
lua_pushstring(L, "key");
int re = lua_pcall(L,
                   1,//参数个数
                   0,//返回值个数
                   0);//错误处理函数在栈中的位置
printf("++++top is %d \n", lua_gettop(L));//检查堆栈情况
```

```lua
function event(e)
    print("c++ call lua function")
    print("e:" .. e)
end
```

### 传递表

```c++
printf("----top is %d \n", lua_gettop(L));
int errfun = lua_gettop(L);
lua_getglobal(L, "event");
lua_pushstring(L, "key");

lua_newtable(L);
lua_pushstring(L, "name");
lua_pushstring(L, "zhangsan");
lua_settable(L, -3);
int re = lua_pcall(L,
                   2,//参数个数
                   0,//返回值个数
                   0);//错误处理函数在栈中的位置，传0的话出错将错误信息置入栈顶
printf("++++top is %d \n", lua_gettop(L));//检查堆栈情况
```

```lua
function event(e,obj)
    print("c++ call lua function")
    print("e:" .. e)
    print(obj["name"])
end
```



## 4-4 C++获取Lua函数的返回值

```c++
cout << "栈顶:" << lua_gettop(L) << endl;

lua_getglobal(L, "event");
lua_pcall(L, 0, 1, 0);//执行成功Lua将返回值入栈
lua_getfield(L, -1, "id");
int id = lua_tonumber(L, -1);
cout << "id:" << id << endl;
lua_pop(L, 1);
lua_pop(L, 1);

cout << "栈顶:" << lua_gettop(L) << endl;
```

```lua
function event()
    return {["id"] = 996}
end
```

## 4-5 C++调用Lua函数错误显示和Lua堆栈清理

### 默认错误处理函数
```c++
printf("----top is %d \n", lua_gettop(L));
lua_getglobal(L, "event");
int re = lua_pcall(L,
                   0,//参数个数
                   0,//返回值个数
                   0);
if (re != 0)
{
    printf("call event failed %s", lua_tostring(L, -1));//不传错误处理函数，会把错误信息压入栈顶
    lua_pop(L, 1);
}
printf("++++top is %d \n", lua_gettop(L));//检查堆栈情况
```

```lua
function event1()
    print("c++ call lua function")
end
```

### 自定义错误处理函数

```c++
printf("----top is %d \n", lua_gettop(L));
lua_getglobal(L, "ferror");
int errfun = lua_gettop(L);
lua_getglobal(L, "event");
int re = lua_pcall(L,
                   0,//参数个数
                   0,//返回值个数
                   errfun);//错误处理函数在栈中的位置，传0的话出错将错误信息置入栈顶
if (re != 0)
{
    printf("call event failed %s", lua_tostring(L, -1));//错误信息压入栈顶
    lua_pop(L, 1);
}
else //执行成功才能获取返回值
{
    //printf("lua return:%s \n", lua_tostring(L,-1));
    //lua_pop(L, 1);
}
lua_pop(L, 1);//函数ferror出栈
printf("++++top is %d \n", lua_gettop(L));//检查堆栈情况
```

```lua
-- Lua 里不定义event函数，让c++出错
function ferror(e)
    print("My error:" .. e)
    return "Lua change error!"
end
-- 不定义event函数，让C++出错
```



## 4-6 完整示例代码

给Lua传入参数、获取Lua返回值、自定义错误处理

```c++
printf("----top is %d \n", lua_gettop(L));
lua_getglobal(L, "ferror");
int errfun = lua_gettop(L);
lua_getglobal(L, "event");
lua_pushstring(L, "key");

lua_newtable(L);
lua_pushstring(L, "name");
lua_pushstring(L, "zhangsan");
lua_settable(L, -3);
int re = lua_pcall(L,
                   2,//参数个数
                   1,//返回值个数
                   errfun);//错误处理函数在栈中的位置，传0的话出错将错误信息置入栈顶
if (re != 0)
{
    printf("call event failed %s", lua_tostring(L, -1));//不传错误处理函数，会把错误信息压入栈顶
    lua_pop(L, 1);
}
else //执行成功才能获取返回值
{
    //printf("lua return:%s \n", lua_tostring(L,-1));
    lua_getfield(L, -1, "id");
    printf("return table id is %d\n", (int)lua_tonumber(L, -1));
    lua_pop(L, 2);
}
lua_pop(L, 1);//函数ferror出栈
printf("++++top is %d \n", lua_gettop(L));//检查堆栈情况
```

```lua
function ferror(e)
    print("My error:" .. e)
    return "Lua change error!"
end
function event(e,obj)
    print("c++ call lua function")
    print("e:" .. e)
    print(obj["name"])
    --return "lua event return"
    local re = {["id"] = 123}
    return re
end
```



# 第5章 C++和Lua结合MFC实战

## 5-1 Lua&MFC项目建立并初始化

+ 通过Lua配置窗口大小
+ 通过Lua弹出提示窗口
+ 通过Lua载入文件并在MFC中显示



```c++
extern "C"
{
#include <lua.h>
#include <lauxlib.h>
#include <lualib.h>
}

lua_State *L = nullptr;
static CMfcLuaDlg *dlg = nullptr;
BOOL Cmy_lua_mfcDlg::OnInitDialog()//初始化函数
{
	CDialogEx::OnInitDialog();

	// 设置此对话框的图标。  当应用程序主窗口不是对话框时，框架将自动
	//  执行此操作
	SetIcon(m_hIcon, TRUE);			// 设置大图标
	SetIcon(m_hIcon, FALSE);		// 设置小图标
    
	// TODO:  在此添加额外的初始化代码
    dlg = this;
    L = lua_open();
    luaL_openlibs(L);
    if (luaL_loadfile(L,"mymfc.lua"))
    {
        printf("loadfile failed %s\n", lua_tostring(L,-1));
        return TRUE;
    }
    if (lua_pcall(L,0,0,0))
    {
        printf("lua_pcall failed %s\n", lua_tostring(L, -1));
        return TRUE;
    }
    return TRUE;  // 除非将焦点设置到控件，否则返回 TRUE
}
```



## 5-2 Lua和MFC结合值接口开放

```c++
lua_getglobal(L, "width");
int w = lua_tonumber(L, -1);

lua_getglobal(L, "height");
int h = lua_tonumber(L, -1);
lua_pop(L, 2);

this->MoveWindow(0, 0, w, h);
```

```lua
width = 1080
height = 769
```

## 5-3 Lua&MFC项目完成和课程总结

```c++
// lua调用来获取控件文本
int GetText(lua_State* L)
{
    int id = lua_tonumber(L, -1);
    CString path;
    dlg->GetDlgItem(id)->GetWindowTextW(path);
    USES_CONVERSION;
    char* txt = W2A(path);
    lua_pushstring(L, txt);
    return 1;
}

int SetText(lua_State* L)
{
    int id = lua_tonumber(L, -2);
    const char* content = lua_tostring(L, -1);
    USES_CONVERSION;
    dlg->GetDlgItem(id)->SetWindowTextW(A2W(content));
    return 0;
}

// 在BOOL CMfcLuaDlg::OnInitDialog()里注册C++函数，luaL_loadfile之前
lua_register(L, "GetText", GetText);
lua_register(L, "SetText", SetText);

//鼠标事件调用Lua函数处理
void CMfcLuaDlg::OnBnClickedLoad()
{
    // TODO:  在此添加控件通知处理程序代码
    lua_getglobal(L, "load");
    lua_pcall(L, 0, 0, 0);
}

```

```lua
function load()
-- 获取文件名
    local fileName = GetText(pathID)
    local fp = io.open(fileName, "rb")
    local content = fp:read("*all")
    SetText(contentID, content)
-- 打开文件 读取内容
-- 设置内容
end
```



##  5-4 课程总结

+ 学习目的：能够开始应用，理解基本原理
+ 学习Lua基本语法
+ 学习Lua调用C++的方法
+ 学习C++调用Lua的方法
+ 以MFC实例来应用Lua
+ Lua与C++混合开发时，用lua decode编辑器调试Lua代码





# 引起堆栈变化的函数

```c++
lua_getfield()
lua_getglobal()
lua_pcall出错时将错误信息入栈
```

