# 第一章 centos内核编译



## 1.1 内核版本

内核版本为5.8





## 1.2 编译过程

1. 安装依赖

   ```shell
   yum install gcc gcc-c++ make ncurses-devel openssl-devel elfutils-libelf-devel bison flex -y
   ```

2. 编译

   ```shell
   # STEP-1 配置 进入UI 界面,方向键切换到save直接保存
   make menuconfig
   
   
   # STEP-2 修改配置文件
   CONFIG_DEBUG_INFO_BTF=n
   CONFIG_SYSTEM_TRUSTED_KEYS=""
   
   # STEP-3 编译
   make
   make modules
   make modules_install
   make install
   ```

3. 查看内核版本

   ```shell
   uname -r
   ```

   





# 第二章 qemu编译



## 2.1 qemu版本

开发选用5.2版本



## 2.2 安装依赖

```shell
yum install python3

# 安装ninja 和 meson
pip3 install ninja
pip3 install meson

# 用法 生成build目录
meson build

cd ./build

# 编译
ninja 

# 安装
ninja install
```





