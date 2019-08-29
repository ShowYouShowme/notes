1. 安装wget

   ```shell
   yum install -y wget 
   ```

2. 设置阿里源

   ```shell
   mv /etc/yum.repos.d/CentOS-Base.repo /etc/yum.repos.d/CentOS-Base.repo.backup
   wget -O /etc/yum.repos.d/CentOS-Base.repo http://mirrors.aliyun.com/repo/Centos-7.repo
   yum makecache
   ```

3. 安装git、vim、ifconfig

   ```shell
   yum install -y git vim net-tools telnet glibc-devel gcc-c++ gcc ncurses-devel zlib-devel perl perl-Module-Install.noarch flex bison
   ```

4. 下载Tars项目并切换到V1.6

   ```shell
   git clone https://github.com/TarsCloud/Tars.git --recursive
   cd ./Tars
git checkout v1.6.0
   ```
   
   

