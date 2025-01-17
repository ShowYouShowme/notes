# 第一章 显卡驱动安装

```shell
# 查看显卡型号
lspci | grep -i vga

## AMD 显卡
06:00.0 VGA compatible controller: Advanced Micro Devices, Inc. [AMD/ATI] Device 1638 (rev c9)

### 检查是否装了nouveau
lsmod | grep nouveau  # 这个驱动非常不稳定

###  AMD显卡查看系统需要安装的驱动
sudo ubuntu-drivers devices  # 我的机器返回是空，即不需要安装任何驱动。装了Chrome，vscode，typora, 搜狗输入法 系统运行非常稳定，不会花屏也不会死机，系统版本是ubuntu 20.04
# (注意：软件包里面的vscode中文输入，只能英文输入)



## NVIDIA 显卡
01:00.0 VGA compatible controller: NVIDIA Corporation Device 1f06 (rev a1)


## NVIDIA 显卡驱动安装流程
############################### 禁用已有显卡驱动
# 检查是否安装Nouveau驱动
lsmod | grep nouveau  # 网上说这个驱动非常不稳定,和chrome一起使用会出问题，实际使用确实如此

# 如果安装了需要禁用
sudo vim /etc/modprobe.d/blacklist.conf
## 加入下面两行
blacklist nouveau
options nouveau modeset=0

# 更新
sudo update-initramfs -u

# 重启设备
reboot

# 检查禁用是否成功
lsmod | grep nouveau  # 没有输出说明禁用成功

################################### 安装系统推荐显卡驱动

# 检查系统推荐的显卡驱动
sudo ubuntu-drivers devices

# 安装显卡驱动
sudo apt install nvidia-driver-415


# 重启电脑，查看显卡驱动
nvidia-smi
```



# 第二章 安装google输入法

```shell
# ubuntu 20.04
sudo apt-get install fcitx-googlepinyin -y

# 设置键盘输入法系统为fcitx

# 重启系统，点击右上角键盘图标进行配置
```





# 第一章 ubuntu 18.04

1. 设置网卡

   1. 编辑配置文件

      ```shell
      sudo vim /etc/netplan/50-cloud-init.yaml
      ```

   2. 配置文件内容

      ```shell
      network:
          ethernets:
              enp0s5:
                  dhcp4: false
                  addresses:
                  - 192.168.0.79/24
                  gateway4: 192.168.0.1
                  nameservers:
                      addresses:
                      - 223.6.6.6
                      - 223.5.5.5
                      search: []
          version: 2
      ```

   3. 重启网卡

      ```shell
      sudo netplan apply
      ```

2. 安装openssh

   ```shell
   # 安装服务
   apt-get install openssh-server
   
   # 查看服务是否已经启动
   ps -ef | grep sshd
   ```

3. live安装系统时设置阿里源

   ```shell
   http://mirrors.aliyun.com/ubuntu/
   ```

4. 启用root账号

   1. 开启root账号

      ```shell
      sudo passwd -u root
      ```

   2. 为root账号设置密码

      ```shell
      sudo passwd root
      ```

   3. 切换到root账号

      ```shell
      su -
      ```

   4. ssh允许root账户登陆

      ```shell
      vim /etc/ssh/sshd_config
      
      PermitRootLogin yes
      
      # 重启ssh服务
      service sshd restart
      ```

      

# 第二章 ubuntu 20

## 2.1 配置阿里源

```shell
# ubuntu desktop 推荐此方法
软件和更新 --> 下载自 --> 选择阿里源
```



## 2.2 升级系统

```shell
# ubuntu 升级系统后会变稳定,减少崩溃几率
duso apt full-upgrade
```



## 2.3 常见问题

1. 如果是NVIDIA显卡，必须禁用开源驱动noveau，再用apt安装显卡驱动，否则会导致一系列的问题

   ```shell
   # 问题一
   chrome 浏览器崩溃
   
   # 问题二
   登录界面死循环
   
   # 问题三
   花屏
   
   # 问题四
   ......
   ```

   





## 2.4 常见操作

***

1. 进入虚拟终端

   ```shell
   Ctrl + Alt + F1 : 图形化登陆界面
   
   Ctrl + Alt + F2 : 当前图形化界面
   
   Ctrl + Alt + F3-F6 : 命令行虚拟终端
   
   Ctrl + Alt + F7-F12 : 另外的虚拟终端，没有任何程序执行
   ```

2. 重启

   ```shell
   reboot 
   # 或者
   shutdown -r 
   ```

3. deb bao anzhuang

   ```shell
   sudo dpkg -i ${package}
   
   # ruguo queshao yilai 
   sudo apt-get -f install # buxuyao zai zhixing dpkg le,yijing zhuanghaole 
   ```

4. 安装搜狗输入法

   ```shell
   apt-get install fcitx 	# 安装输入法系统
   sudo curl -sL 'https://keyserver.ubuntu.com/pks/lookup?&op=get&search=0x73BC8FBCF5DE40C6ADFCFFFA9C949F2093F565FF' | sudo apt-key add
   sudo apt-add-repository 'deb http://archive.ubuntukylin.com/ukui focal main'
   sudo apt upgrade
   sudo apt install sogouimebs
   sogouIme-configtool 	# 输入法配置
   
   # 重启电脑，用Ctrl + Space 切换输入法， 右上角有搜狗的图标
   ```

   

# 第三章 常用快捷键

   ## 3.1 桌面快捷键

***

   ```
   Alt + F1：聚焦到桌面左侧任务导航栏，可按上下键进行导航
   Alt + F2：运行命令
   Alt + F4：关闭当前窗口
   Alt + Tab：切换程序窗口
   Alt + 空格：打开窗口菜单
   PrtSc：桌面截图
   Win + A：搜索/浏览程序
   Win + F：搜索/浏览文件
   Win + M：搜索/浏览音乐文件
   Win：搜索/浏览程序、文件、音乐文件等
   ```

   

   ## 3.2 终端快捷键

***

   ```
   Ctrl + Alt + T：打开终端
   Tab：命令或文件名自动补全
   Ctrl + Shift + C：复制
   Ctrl + Shift + V：粘贴
   Ctrl + Shift + T：在同一个窗口新建终端标签页
   Ctrl + Shift + W：关闭标签页
   Ctrl + Shift + N：新建终端窗口
   Ctrl + Shift + Q：关闭终端窗口
   Ctrl + Shift + PageUp：标签页左移
   Ctrl + Shift + PageDown：标签页右移
   Ctrl + D：关闭标签页
   Ctrl + L：清除屏幕
   Ctrl + C：终止当前任务
   Ctrl + P：显示上一条历史命令
   Ctrl + N：显示下一条历史命令
   Ctrl + R：反向搜索历史命令
   Ctrl + J/M：回车（同enter键功能）
   Ctrl + A：光标移动到行首
   Ctrl + E：光标移动到行尾
   Ctrl + B：关闭想后移动一个位置（backward）
   Ctrl + Z：把当前任务放到后台运行
   Ctrl + PageUp：前一个终端标签页
   Ctrl + PageDown：下一个终端标签页
   F1：打开帮助指南
   F11：全屏切换
   Alt + F：打开“文件”菜单（file）
   Alt + E：打开“编辑”菜单（edit）
   Alt + V：打开“查看“菜单（view）
   Alt + S：打开“搜索”菜单（search）
   Alt + T：打开“终端”菜单（terminal）
   Alt + H：打开“帮助”菜单（help）
   Ctrl + →：光标移动到上一个单词的词首
   Ctrl + ←：光标移动到下一个单词的词尾
   Ctrl + T：将光标位置的字符和前一个字符进行位置交换
   Ctrl + U：剪切从行的开头到光标前一个位置的所有字符
   Ctrl + K：剪切从光标位置到行末的所有字符
   Ctrl + Y：粘贴Ctrl + U/Ctrl + K剪切的内容
   Ctrl + H/*：删除光标位置的前一个字符（backspace键功能）
   Ctrl + D：删除光标位置的一个字符（delete键功能）
   Ctrl + W：删除光标位置的前一个单词（Alt + Backspace组合键功能）
   Ctrl + &：恢复Ctrl + H/D/W删除的内容
   Ctrl + Win + ↑：最大化当前窗口
   Ctrl + Win + ↓：还原/最小化当前窗口
   Ctrl + Win + D：最小化所有窗口
   Win + W：展示所有窗口
   Win + T：打开回收站
   2次连续Tab/4次连续Esc/2次连续Ctrl + I：将显示所有命令和工具名称
   ```

   

   ## 3.3 Gedit快捷键

***

   ```
   Ctrl + N：新建文档
   Ctrl + W：关闭文档
   Ctrl + S：保存文档
   Ctrl + Shift + S：另存为
   Ctrl + F：搜索
   Ctrl + H：搜索并替换
   Ctrl + I：跳到某一行
   Ctrl + C：复制
   Ctrl + V：粘贴
   Ctrl + X：剪切
   Ctrl + Q：退出
   ```

   

# 第五章 init命令

***

```shell
#需要用root权限
0：关机
1：救援模式，重置密码进入
2：不带网络的多用户模式
3：字符终端多用户  #常用
4：未使用
5：图形模式      #常用
6：重启
```





# 第六章 常用命令

***



## 6.1 APT

***

1. 查看已安装的软件

   ```shell
   apt list --installed
   ```

2. apt 和 apt-get对比

   |     apt 命令     |      取代的命令      |           命令的功能           |
   | :--------------: | :------------------: | :----------------------------: |
   |   apt install    |   apt-get install    |           安装软件包           |
   |    apt remove    |    apt-get remove    |           移除软件包           |
   |    apt purge     |    apt-get purge     |      移除软件包及配置文件      |
   |    apt update    |    apt-get update    |  刷新存储库索引(更新软件有源)  |
   |   apt upgrade    |   apt-get upgrade    |     升级所有可升级的软件包     |
   |  apt autoremove  |  apt-get autoremove  |       自动删除不需要的包       |
   | apt full-upgrade | apt-get dist-upgrade | 在升级软件包时自动处理依赖关系 |
   |    apt search    |   apt-cache search   |          搜索应用程序          |
   |     apt show     |    apt-cache show    |           显示装细节           |

3. apt自己的命令

   |   新的apt命令    |              命令的功能              |
   | :--------------: | :----------------------------------: |
   |     apt list     | 列出包含条件的包（已安装，可升级等） |
   | apt edit-sources |              编辑源列表              |

4. 建议使用apt替代apt-get

5. 安装本地deb包

   ```shell
   sudo apt install -y ./teamviewer_amd64.deb
   ```

6. 列出已安装的软件包

   ```shell
   apt list --installed
   ```

7. 卸载软件

   ```shell
   apt purge  # 连同配置文件一起删除
   ```

   



## 6.2 制作u盘启动盘

***



### 6.3.1 使用dd命令制作

***

1. 查看u盘设备

   ```shell
   lsblk
   
   sda           8:0    1  28.9G  0 disk 
   └─sda4        8:4    1  28.9G  0 part /media/nash/Ubuntu 20.0 #sda4是u盘sda的分区
   nvme0n1     259:0    0   477G  0 disk 
   ├─nvme0n1p1 259:1    0   512M  0 part /boot/efi
   └─nvme0n1p2 259:2    0 476.4G  0 part /
   
   #或者
   sudo fdisk -l
   ```

2. 卸载u盘

   ```shell
   sudo umount /dev/sda
   ```

3. 使用dd命令写入数据

   ```shell
   sudo dd if=./ubuntu-20.04.2.0-desktop-amd64.iso of=/dev/sda
   
   #制作完成提示信息
   记录了5619584+0 的读入
   记录了5619584+0 的写出
   2877227008字节（2.9 GB，2.7 GiB）已复制，323.943 s，8.9 MB/s
   ```




### 6.3.2 使用启动盘创建器制作

***

1. 开始-->所有程序-->启动盘创建器
2. 选择系统镜像（仅仅支持debian系列的系统）
3. 选择u盘
4. 点击制作启动盘



## 6.3 切换到管理员

***

```shell
sudo su
```



## 6.4 未满足的依赖关系

### 原因

1. 软件依赖于某一软件旧的版本，可是你却已经安装了新的。

2. 要装A， 依赖B, 但是已经安装的软件C也依赖B， 但是A依赖的B的版本和C依赖的B的版本不一致， 导致了如果要安装B，那么C便不能正常运行了，所以系统报错。



### 解决方案

使用apt purge 移除软件包，再安装即可



```shell
下列软件包有未满足的依赖关系：
 libqt4-opengl : 依赖: libqtcore4 (= 4:4.8.3+dfsg-0ubuntu3) 但是 4:4.8.3+dfsg-0ubuntu3.1 正要被安装
                 依赖: libqtgui4 (= 4:4.8.3+dfsg-0ubuntu3) 但是 4:4.8.3+dfsg-0ubuntu3.1 正要被安装
E: 无法修正错误，因为您要求某些软件包保持现状，就是它们破坏了软件包间的依赖关系。


# step-1 删除已经存在的软件包
sudo apt purge libqtcore4
sudo apt purge libqtgui4

# step-2 再次安装即可
```





# 第七章 包管理器



## 7.1 dpkg

1. 查看软件包安装了哪些文件

   ```shell
   dpkg -L redis-tools
   ```

2. 安装deb包

   ```shell
   dpkg -i ${package}
   ```

3. 删除软件包

   ```shell
   # [不推荐使用]不删除配置文件，下次安装该软件时不会重新创建配置文件
   dpkg -r ${package}
   
   # 或者 会同时删除配置文件，[推荐建议使用]
   dpkg -P ${package}
   ```

4. 查看已经安装的软件包

   ```shell
   dpkg -l  # 可以类似vim操作，比如翻页，查找
   ```

   

