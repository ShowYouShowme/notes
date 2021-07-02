# 第一章 使用devtoolset升级



## 1.1 升级到7.3

```shell
yum -y install centos-release-scl
yum -y install devtoolset-7-gcc devtoolset-7-gcc-c++ devtoolset-7-binutils

# scl命令启用只是临时的，退出shell或重启就会恢复原系统gcc版本
scl enable devtoolset-7 bash

# 长期使用
echo "source /opt/rh/devtoolset-7/enable" >>/etc/profile
```





## 1.2 升级到8.3

```shell
yum -y install centos-release-scl
yum -y install devtoolset-8-gcc devtoolset-8-gcc-c++ devtoolset-8-binutils
# scl命令启用只是临时的，退出shell或重启就会恢复原系统gcc版本
scl enable devtoolset-7 bash

# 长期使用
echo "source /opt/rh/devtoolset-8/enable" >>/etc/profile
```





## 1.3 升级到9.3

```shell
yum -y install centos-release-scl
yum -y install devtoolset-9-gcc devtoolset-9-gcc-c++ devtoolset-9-binutils
# scl命令启用只是临时的，退出shell或重启就会恢复原系统gcc版本
scl enable devtoolset-9 bash

# 长期使用
echo "source /opt/rh/devtoolset-9/enable" >>/etc/profile
```





# 第二章 使用Docker

C++ 的server 部署在Docker 里面可以确保环境一致，避免很多问题。这是非常推荐的做法。