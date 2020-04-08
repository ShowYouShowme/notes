# ubuntu18.04

1. 设置网卡

   + 配置网卡信息

     ```shell
     # sudo vim /etc/network/interfaces
     
     iface enp0s5 inet static # enp0s5是网卡名,用ifconfig获取
     address 210.72.92.25
     gateway 210.72.92.254
     netmask 255.255.255.0
     dns-nameservers 8.8.8.8
     ```

   + 重启网卡

     ```shell
     sudo ifconfig enp0s5 down
     sudo ifconfig enp0s5 up
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

      

   