# 安装Samba

```shell
yum -y install samba
```



# Samba相关操作

```shell
# 启动服务
systemctl start smb.service

# 重启服务
service smb restart

# 设置开机启动
chkconfig smb on
```



# Samba配置

```shell
vim /etc/samba/smb.conf
#加入以下配置
[FileShare]
comment = share some files
path =/root
public= yes 
writeable = yes 
create mask =0644
browseable=yes
directory mask =0755
```



# 添加用户

1. 创建共享目录并设置权限

   ```shell
   mkdir /opt/students
   chmod 777 /opt/students
   ```

2. 添加用户并设置密码

   ```shell
   useradd -s /sbin/nologin zhangsan
   passwd zhangsan 
   
   useradd -s /sbin/nologin lisi
   passwd lisi 
   ```

3. 将系统用户zhangsan、lisi添加为samba用户并设置samba用户登录密码

   ```shell
   smbpasswd -a zhangsan
   smbpasswd -a lisi
   ```

4. 查看samba用户

   ```
   pdbedit -L
   ```

5. 重启smb服务

   ```shell
   service smb restart
   ```

   

# Samba 访问失败

1. 确保CentOS防火墙已经关闭

   ```shell
   # 查看防火墙状态
   firewall-cmd --state
   
   # 停止防火墙
   systemctl stop firewalld.service
   
   # 禁止firewall开机启动
   systemctl disable firewalld.service 
   ```

2. 确保smb.conf配置文件正确，可以执行`testparm`来检验

3. 确保SELinux已经关闭

   ```shell
   # 查看SELinux状态
   getenforce
   
   # 临时关闭SELinux
   setenforce 0
   
   # 永久关闭SELinux
   vim /etc/selinux/config 
   SELINUX=permissive
   ```

   