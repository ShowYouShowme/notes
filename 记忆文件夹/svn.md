# 第一章 安装

1. 安装服务

   ```shell
   yum -y install subversion
   ```

2. 创建项目根目录

   ```shell
   mkdir /home/roglic/svn/repository
   ```

3. 创建svn项目

   ```shell
   cd /home/roglic/svn/repository
   svnadmin create art
   ```

4. 修改配置文件

   ```shell
   cd art/conf
   
   #配置账号密码
   vim passwd
   
   [users]
   harry = harryssecret
   sally = sallyssecret
   fuzhenkui = fuzhenkui123
   panda = panda123
   dujingna = dujingna258
   liaojiahui = liaojiahui369
   
   vim authz
   #配置分组和权限
   [groups]
   harry_and_sally = harry,sally,panda,dujingna,liaojiahui
   fron_end = fuzhenkui
   
   [/]
   @harry_and_sally = rw
   @fron_end = r
   
   #修改项目设置
   vim svnserver.conf 
   
   [general]
   #none|read|write none 表示无访问权限，read 表示只读，write 表示可读可写，默认为 read
   #非授权用户的访问级别
   anon-access = none
   #授权用户的访问级别
   auth-access = write
   #指定账号密码数据库文件名
   password-db = passwd
   #指定权限配置文件名
   authz-db = authz
   #登录时提示的提示信息
   realm =this is nash's project
   ```

5. 启动服务

   ```shell
   svnserve -d -r $HOME/svn/repository
   ```

6. 用TortoiseSVN下注

   ```ini
   url = svn://192.168.2.102/art
   ```

   

