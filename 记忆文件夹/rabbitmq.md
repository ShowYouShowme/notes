# 第一章 安装

```python
# 安装erlang
yum install -y socat
wget https://github.com/rabbitmq/erlang-rpm/releases/download/v23.3.2/erlang-23.3.2-1.el7.x86_64.rpm
rpm -ivh erlang-23.3.2-1.el7.x86_64.rpm

# 安装RabbitMQ
wget https://github.com/rabbitmq/rabbitmq-server/releases/download/v3.8.14/rabbitmq-server-3.8.14-1.el7.noarch.rpm
rpm -ivh rabbitmq-server-3.8.14-1.el7.noarch.rpm
```





# 第二章 基础知识

1. 安装后配置

   ```shell
   # 开启管理后台
   rabbitmq-plugins enable rabbitmq_management
   
   # 创建管理后台账户
   # Rabbitmq从3.3.0开始默认用户(guest/guest)只能通过除localhost的访问，我们自己创建登录用户并授权管理员登录。执行下面三条命令即可创建一个可以远程登录管理后台的账户
   rabbitmqctl add_user test 123456
   rabbitmqctl  set_user_tags  test  administrator
   rabbitmqctl set_permissions -p "/" test ".*" ".*" ".*"
   
   
   # 登录管理后台
   http://${ip}:15672/
   ```

2. 服务管理

   ```python
   # rabbitmq的工作目录 /var/lib/rabbitmq
   # 使用systemctl管理服务
   systemctl start rabbitmq-server #启动服务
   # 或者
   /usr/sbin/rabbitmq-server
   
   
   systemctl status rabbitmq-server #查看服务状态
   
   
   systemctl stop rabbitmq-server #停止服务
   # 或者
   /usr/sbin/rabbitmqctl shutdown
   
   
   systemctl enable rabbitmq-server #开机启动服务
   
   # 关闭服务
   rabbitmqctl stop_app
   
   # 启动服务
   rabbitmqctl start_app
   
   # 重置服务
   rabbitmqctl reset
   ```

3. vhost操作

   ```python
   #添加vhost,必须对用户授权才能访问
   rabbitmqctl add_vhost testHost
    
   #列出vhost
   rabbitmqctl list_vhosts
    
   #删除vhost
   rabbitmqctl delete_vhost testHost
   ```

4. 权限管理

   ```python
   #rabbitmqctl set_permissions [-p vhost] {user} {conf} {write} {read}
   #vhost 授予用户访问权限的vhost名称 默认 /
   #user 可以访问指定vhost的用户名
   #conf 一个用于匹配用户在那些资源上拥有可配置的正则表达式
   #write 一个用于匹配用户在那些资源上拥有可写的正则表达式
   #read 一个用于匹配用户在那些资源上拥有可读的正则表达式
    
   #授予admin用户可访问虚拟主机testhost，并在所有的资源上具备可配置、可写及可读的权限
   rabbitmqctl set_permissions -p testHost admin ".*" ".*" ".*"
    
   #授予admin用户可访问虚拟主机testhost1，在以queue开头的资源上具备可配置权限、并在所有的资源上可写及可读的权限
   rabbitmqctl set_permissions -p testHost admin "^queue.*" ".*" ".*"
    
   #清除权限
   rabbitmqctl clear_permissions -p testHost admin
    
   #虚拟主机的权限
   rabbitmqctl list_permissions -p testHost
    
   #用户权限
   rabbitmqctl list_user_permissions admin
   ```

5. 用户管理

   ```python
   # 创建用户
   rabbitmqctl add_user test 123456
   
   # 修改密码
   rabbitmqctl change_passwd test 789456
   
   # 列出用户
   rabbitmqctl list_users
   ```

6. 用户角色

   + Administrator：超级管理员，可登陆管理控制台(启用management plugin的情况下)，可查看所有的信息，并且可以对用户，策略(policy)进行操作，因为是超级管理员，可以这样理解，它可以为所欲为，什么操作都能干，删除用户、修改用户密码、重置用户角色、策略制定等等
   + Monitoring：监控者，可登陆管理控制台(启用management plugin的情况下)，同时可以查看rabbitmq节点的相关信息(进程数，内存使用情况，磁盘使用情况等)
   + Policymake：策略制定者，可登陆管理控制台(启用management plugin的情况下)，同时可以对policy进行管理。但无法查看节点的相关信息
   + Management：普通管理者，仅可登陆管理控制台(启用management plugin的情况下)，无法看到节点信息，也无法对策略进行管理
   + Impersonator：模拟者，无法登录管理控制台，因为没有管理者权限
   + None：其他用户，无法登陆管理控制台，通常就是普通的生产者和消费者。代码里就用这种角色的账号登录

7. 其它命令

   + 列出全部交换机

     ```shell
     sudo rabbitmqctl list_exchanges
     ```

   + 列出全部绑定

     ```shell
     rabbitmqctl list_bindings
     ```




# 第三章 注意事项

1. 创建自定义vHost时，名字为gateway 而不是 /gateway

2. 访问名称为gateway的vHost时url如下

   ```python
   amqp://test:123456@192.168.1.49:5672/gateway
   
   # 访问vHost为/的url
   amqp://test:123456@192.168.1.49:5672/
   ```

   



