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

### 2.1.1 方法一

```shell
# vim /etc/apt/source.list
deb http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal main restricted universe multiverse
 
deb http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-security main restricted universe multiverse
 
deb http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-updates main restricted universe multiverse
 
deb http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-proposed main restricted universe multiverse
 
deb http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
deb-src http://mirrors.aliyun.com/ubuntu/ focal-backports main restricted universe multiverse
```



### 2.1.2 方法二

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

***

1. chrome会导致系统崩溃：建议使用firefox
2. ubuntu crash 时，找出导致crash的软件，不使用即可
3. vscode 从官网下载deb包安装，商店里面安装的无法输入中文
4. 关闭qemu后，系统变得非常稳定了





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

   



# 第四章 gnome-shell



## 4.1 重启gnome-shell

gnome-shell用一段时间就会卡死，需要重启

***

1. 方法一

   ```shell
   ALT + F2
   输入r，然后按下回车
   ```

2. 方法二

   ```shell
   killall -3 gnome-shell
   ```

3. 方法三

   ```shell
   #会导致全部gui程序关闭,不推荐
   /etc/init.d/gdm3 restart
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
   |    apt update    |    apt-get update    |         刷新存储库索引         |
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
