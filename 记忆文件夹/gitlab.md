# 第一章 安装

```shell
# 系统 ubuntu 20.04LTS
# gitlab 内存占用非常高
curl -s https://packages.gitlab.com/install/repositories/gitlab/gitlab-ce/script.deb.sh | sudo bash
sudo apt-get install gitlab-ce

# 配置文件
/etc/gitlab/gitlab.rb

# 常用命令
sudo gitlab-ctl reconfigure # 修改配置后使用

sudo gitlab-ctl restart # 重启服务

sudo gitlab-ctl status # 查看服务状态

sudo gitlab-ctl stop # 停止服务

# root用户初始化密码
cat /etc/gitlab/initial_root_password

# 配置服务绑定的地址
external_url 'http://192.168.0.106'


# 开机启动
sudo systemctl enable gitlab-runsvdir.service

# 禁止开机启动
sudo systemctl disable gitlab-runsvdir.service
```

