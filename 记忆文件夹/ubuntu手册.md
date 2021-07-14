# ubuntu18.04

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

      


# Ubuntu 20



## 配置阿里源

### 方法一

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



### 方法二

```shell
# ubuntu desktop 推荐此方法
软件和更新 --> 下载自 --> 选择阿里源
```



## 升级系统

```shell
# ubuntu 升级系统后会变稳定,减少崩溃几率
duso apt full-upgrade
```



## 常见问题

***

1. chrome会导致系统崩溃：建议使用firefox
2. ubuntu crash 时，找出导致crash的软件，不使用即可





## 常见操作

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

   

   
