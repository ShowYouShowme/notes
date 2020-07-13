wget http://nginx.org/download/nginx-1.16.1.tar.gz
tar -zxvf nginx-1.16.1.tar.gz
cd ./nginx-1.16.1

# nginx配置文件在VIM中高亮
mkdir ~/.vim/
cp -r ./contrib/vim/* ~/.vim/

yum install gcc pcre pcre-devel zlib zlib-devel openssl openssl-devel -y


./configure --prefix=/usr/local/nginx/

make -j4


make install



## nginx 的配置修改

##        location / {
##            root   html;
##            autoindex on;   ## 加上这条即可显示文件夹
##            index  index.html index.htm;
##        }



# 配置nginx的 tcp反向代理

# configure 时 加上--with-stream这个参数，以加载ngx_stream_core_module这个模块
# 监听本机的2222端口，实现跳转到192.168.56.12的22号端口
stream {
upstream tcp_proxy{
hash $remote_addr consistent;
server 192.168.56.12:22;
}

server {
listen 2222 so_keepalive=on;
proxy_connect_timeout 1s;
proxy_timeout 3s;
proxy_pass tcp_proxy;
}
}
