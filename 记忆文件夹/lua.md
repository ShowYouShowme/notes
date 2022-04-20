# 第一章 代码提示

```lua
-- 其它脚本语言,比如JavaScript类似
local t2 = {
    id = 123,
    info = {
        gold = 999,
        level = 20,
        mana = 500,
        hp = 80
    }
}

local info = t2.info
info.gold = 555

str = JSON.stringfy(info)
print(str)
```



# 第二章 模块与包



## 2.1 调用动态链接库

1. 编写c语言代码

   ```c
   // sum2.c
   #include <math.h>
   #include <lua.h>
   #include <lauxlib.h>
   #include <lualib.h>
   
   static int ding_sum2(lua_State *L){
       double d1 = luaL_checknumber(L, 1);
       double d2 = luaL_checknumber(L, 2);
       lua_pushnumber(L, d1+d2);
       return 1;
   }
   
   static const struct luaL_Reg ding_lib[] = {
       {"ding_sum2" , ding_sum2},
       {NULL, NULL}
   };
   
   int luaopen_ding_lib(lua_State *L){
       luaL_newlib(L, ding_lib); // 5.2
       //luaL_register(L, "ding_lib",ding_lib); // lua 5.1
       return 1;
   }
   ```

2. 编译为动态链接库

   ```shell
   gcc sum2.c -fPIC -shared -o ding_lib.so
   ```

3. 编写测试

   ```lua
   local mylib = require "ding_lib"
   print(type(mylib))
   print(mylib.ding_sum2(23,17))
   ```



# 第三章 错误处理



## 3.1 error



## 3.2 assert

```lua
assert(type(a) == "number", "a 不是一个数字")
```



## 3.3 pcall



## 3.4 xpcall



## 3.5 debug





# 第四章 excel转换为lua

使用wps的xml作为源文件。

1. 表tab的格式

   ```shell
   # 表名|代码表名
   
   巅峰商城|bestShop
   ```

2. 字段格式

   ```shell
   # 字段名|代码字段名|数据类型
   商品名|productName|string
   ```

3. 特殊值

   ```shell
   # 表格里没有值时用nil表示
   # ''是代码才有的值,excel配置文件没有
   # 每个表格的值先去掉前后空白然后再解析
   
   # 配置文件值只有 int和string，不要存放小数
   ```

4. 客户端修改配置文件流程[不需要开发干预]

   ```shell
   # step-1
   导出lua
   
   # step-2
   提交到代码仓库
   
   # step-3
   jenkins自动构建发布
   ```

   
