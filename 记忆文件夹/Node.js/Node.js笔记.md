## promise 用法

1. 示例一

```javascript
function __settimeout(ms : number):Promise<void>{
    return new Promise<void>((resolve, reject)=>{
        setTimeout(()=>{
            resolve();
        }, ms);
    })
}

async function sync_time_out(){
    await __settimeout(2000);
    console.log("after 2 s!");
}
```

2. 示例二

   ```js
   
   // 函数声明: keys(pattern: string, cb?: Callback<string[]>): R;
   function __keys(pattern : string):Promise<string[]>{
       return new Promise<string[]>((resolve , reject) => {
           redis_client.keys(pattern,(err: Error | null, reply: string[]) : void =>{
               if (err) {
                   reject(err);
               }else{
                   resolve(reply);
               }
           });
       })
   }
   ```

   