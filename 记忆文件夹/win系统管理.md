# 网卡配置

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

   