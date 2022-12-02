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
   cat passwd
   
   [users]
   harry = harryssecret
   sally = sallyssecret
   fuzhenkui = fuzhenkui123
   panda = panda123
   dujingna = dujingna258
   liaojiahui = liaojiahui369
   
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
   anon-access = none
   auth-access = write
   password-db = passwd
   authz-db = authz
   #项目名
   realm =art
   ```

5. 启动服务

   ```shell
   svnserve -d -r /home/roglic/svn/repository
   ```

6. 用TortoiseSVN下注

   ```ini
   url = svn://192.168.2.102/art
   ```

   

