# 第一章 安装

下载地址

```ini
url = https://mirror.lzu.edu.cn/debian-cd/12.6.0/amd64/iso-dvd/debian-12.6.0-amd64-DVD-1.iso

url = https://cdimage.debian.org/debian-cd/current/amd64/iso-cd/debian-12.6.0-amd64-netinst.iso
```



配置国内源

```ini
vi /etc/apt/sources.list

deb http://mirrors.ustc.edu.cn/debian stable main contrib non-free
# deb-src http://mirrors.ustc.edu.cn/debian stable main contrib non-free
deb http://mirrors.ustc.edu.cn/debian stable-updates main contrib non-free
# deb-src http://mirrors.ustc.edu.cn/debian stable-updates main contrib non-free

# deb http://mirrors.ustc.edu.cn/debian stable-proposed-updates main contrib non-free
# deb-src http://mirrors.ustc.edu.cn/debian stable-proposed-updates main contrib non-free
```



更新索引

```shell
apt-get update
```

