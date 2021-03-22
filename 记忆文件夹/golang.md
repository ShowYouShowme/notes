# 第一章 简介



## 1.1 第一个程序

```go
// 文件路径 src/main/hello_world.go
package main // 包，表明代码所在模块

import "fmt"  // 引入依赖
func main()  {
	fmt.Println("Hello World!")
}
```



## 1.2 运行

1. 直接运行

   ```shell
   go run ${file_name}
   ```

2. 编译

   ```shell
   go build ${file_name}
   ```



## 1.3 程序入口

1. 必须是main包：<b style="color:red">package main</b>
2. 必须是main方法：<b style="color:red">func main()</b>
3. 文件名不一定是：<b style="color:red">main.go</b>



## 1.4 退出返回值

1. go中main函数不支持任何返回值
2. 通过<b style="color:red">os.Exit()</b>来返回状态



## 1.5 获取命令行参数

```go
package main

import "fmt"
import "os"
func main()  {
	fmt.Println("Hello World!")

	fmt.Println(os.Args)

	os.Exit(12)
}
```

# 第二章 程序基本结构



# 第三章  常用集合





# 第四章 字符串



# 第五章 函数



# 第六章 面向对象编程



# 第七章 编写好的错误处理



# 第八章 包和依赖管理



# 第九章 并发编程



# 第十章 典型并发任务



# 第十一章 测试



# 第十二章 反射和Unsafe



# 第十三章 常见架构模式的实现



# 第十四章 常见任务



# 第十五章 性能调优



# 第十六章 高可用性服务设计

