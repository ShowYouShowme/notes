# 安装步骤

1. 用UltraISO制作U盘启动盘
2. 在BIOS里面设置Boot Mode为Legacy Only
3. 从U盘启动系统，在grub界面选择Install CentOS 7
4. 在系统-->安装位置里删掉原来的分区，再重新分区最后设置分区大小
   + /boot ：存放与系统启动相关的程序，建议大小100~1024M
   + / ：根目录，尽量多分配空间
   + /home 目录，存放用户数据，多分配空间
   + swap：交换分区，比内存大
5. 开始安装



# 镜像

CentOS-7-x86_64-Minimal-1810.iso