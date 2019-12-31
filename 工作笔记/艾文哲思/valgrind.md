# 安装步骤

1. 下载代码

   ```shell
   wget https://sourceware.org/pub/valgrind/valgrind-3.15.0.tar.bz2
   ```

2. 安装bzip2

   ```shell
   yum install -y bzip2
   ```

3. 编译安装软件

   ```shell
   mkdir /usr/local/valgrind
   tar -jxvf valgrind-3.15.0.tar.bz2
   cd ./valgrind-3.15.0
   ./configure --prefix=/usr/local/valgrind/
   make -j4
   make install
   ```

4. 检测内存泄漏

   ```shell
   /usr/local/valgrind/bin/valgrind --tool=memcheck --leak-check=yes --show-reachable=yes ./main
   ```

   



# 简单使用

1. 代码

   ```cpp
   #include <stdio.h>
   #include <stdlib.h>
    
   void f()
   {
       int *x = malloc(10 * sizeof(int));
       x[10] = 0;
   }
   int main()
   {
       f();
       return 0;
   }
   ```

2. 编译

   ```shell
   gcc -g val.c -o main.out
   ```

3. 内存泄漏检测

   ```shell
   valgrind --tool=memcheck --leak-check=yes --show-reachable=yes ./main.out
   ```

4. 检测结果

   ```shell
   --leak-check=yes --show-reachable=yes ./main.out
   ==16723== Memcheck, a memory error detector
   ==16723== Copyright (C) 2002-2017, and GNU GPL'd, by Julian Seward et al.
   ==16723== Using Valgrind-3.13.0 and LibVEX; rerun with -h for copyright info
   ==16723== Command: ./main.out
   ==16723== 
   ==16723== Invalid write of size 4
   ==16723==    at 0x108668: f (val.c:7)
   ==16723==    by 0x10867E: main (val.c:12)
   ==16723==  Address 0x5857068 is 0 bytes after a block of size 40 alloc'd
   ==16723==    at 0x4C2FB6B: malloc (vg_replace_malloc.c:299)
   ==16723==    by 0x10865B: f (val.c:6)
   ==16723==    by 0x10867E: main (val.c:12)
   ==16723== 
   ==16723== 
   ==16723== HEAP SUMMARY:
   ==16723==     in use at exit: 40 bytes in 1 blocks
   ==16723==   total heap usage: 1 allocs, 0 frees, 40 bytes allocated
   ==16723== 
   ==16723== 40 bytes in 1 blocks are definitely lost in loss record 1 of 1
   ==16723==    at 0x4C2FB6B: malloc (vg_replace_malloc.c:299)
   ==16723==    by 0x10865B: f (val.c:6)
   ==16723==    by 0x10867E: main (val.c:12)
   ==16723== 
   ==16723== LEAK SUMMARY:
   ==16723==    definitely lost: 40 bytes in 1 blocks # 肯定泄漏
   ==16723==    indirectly lost: 0 bytes in 0 blocks  # 间接泄漏
   ==16723==      possibly lost: 0 bytes in 0 blocks  # 可能泄漏
   ==16723==    still reachable: 0 bytes in 0 blocks  # 依旧可达
   ==16723==         suppressed: 0 bytes in 0 blocks  
   ==16723== 
   ==16723== For counts of detected and suppressed errors, rerun with: -v
   ==16723== ERROR SUMMARY: 2 errors from 2 contexts (suppressed: 0 from 0)
   ```

   