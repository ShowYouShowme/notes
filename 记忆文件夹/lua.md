# 第一章 代码提示

```lua
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

   

