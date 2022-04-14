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

