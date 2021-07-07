# 一、网卡配置

1. 查看网卡信息

   ```powershell
   netsh interface ip show address
   ```

2. 查看DNS信息

   ```shell
   netsh interface ip show dns
   ```

3. 配置网卡地址

   ```shell
   netsh interface ip set address name="WLAN" source=static addr=192.168.0.106 mask=255.255.255.0 gateway=192.168.0.1 gwmetric=1
   ```

4. 配置首选DNS

   ```shell
   netsh interface ip add dnsservers "WLAN" 223.6.6.6 index=1 
   ```

5. 配置备用DNS

   ```shell
   netsh interface ip add dnsservers "WLAN" 223.5.5.5 index=2
   ```

6. 网络受限：电脑没有获取到IP地址，可能是路由器DHCP功能未开启或者DHCP功能有问题！电脑手动配置ip + 网关 + dns服务器即可解决！

   ```shell
   # 1: 第一次配置完了刷新网卡信息
   # 2: 如果之前已经配置,但是依旧受限,只需要刷新网卡信息即可
   ipconfig /renew
   ```

   

# 二、 右键菜单



## 2.1 右键点击目录空白处

```shell
# 注册表路径
HKEY_CLASSES_ROOT\Directory\Background\shell

# 1-- 设置菜单名
# 2-- 设置菜单图标
# 3-- 设置执行的命令
```



## 2.2 右键文件

```shell
# 注册表路径
HKEY_CLASSES_ROOT\*

# 1-- 设置菜单名
# 2-- 设置菜单图标
# 3-- 设置执行的命令
```





# 三、C盘太大

> 1. 把全部软件卸载，然后再安装即可
> 2. 系统只有一个C盘，不分区了

