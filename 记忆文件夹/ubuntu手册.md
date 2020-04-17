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

      

   